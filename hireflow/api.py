import frappe
from collections import defaultdict
from frappe.query_builder import DocType
import base64
import json
import os
import mimetypes
from frappe.utils import now_datetime,get_datetime,add_days
def success_message(doc,method):
    frappe.msgprint(f"New {doc.doctype} document with id {doc.name} saved successfully")

@frappe.whitelist()
def get_empid(user:str=None):
    if not user:
        return frappe.get_value("Employee",{"email":frappe.session.user},"name")
    return frappe.get_value("Employee",{"email":user},"name")


@frappe.whitelist()
def employee_dept():
    user=frappe.session.user
    if not user:
        return ""
    return frappe.get_value("Employee",{"email":user},"Department")
    
def approval_reminder():
    
    cut_off = add_days(now_datetime(), -1)

    approvals = DocType("Approval")

    pending_approvals = (
        frappe.qb.from_(approvals)
        .select(
            approvals.approver,
            approvals.expense
        )
        .where(
            (approvals.action == "Submitted") &
            (approvals.creation <= cut_off)
        )
    )
    result = pending_approvals.run(as_dict=True)
    if not result:
        return
    grouped = defaultdict(list)
    for row in result:
        grouped[row["approver"]].append(row["expense"])
    for approver, expenses in grouped.items():
        approver=frappe.get_value("Employee",approver,"email")
        pending_expenses = ", ".join(expenses)
        frappe.new_doc(
            "Notification Log",
            for_user=approver,
            type="Alert",
            subject="Pending Request Reminder",
            email_content=f"""
The following requests were raised a day ago.
This is a reminder to review them soon.

Pending Expenses: {pending_expenses}
"""
        ).insert(ignore_permissions=True)
    frappe.db.commit()
 
def process_expense(expense_name):
    print("Processing expenses")
    expense_doc=frappe.get_doc("Expense",expense_name)
    results={}
    for index,row in enumerate(expense_doc.expenses_table):
        values=frappe.db.get_value("Expense List",row.name,["expense_type","other_expense","date_of_spending","amount","receipt"],as_dict=True)
        print(values)
        results[index]=get_receipt_data(values['receipt'],values)
    print(results)
    reason=[]
    for row,result in results.items():
        if not result.get("is_match"):
            reason.append(result.get("reason", "Unknown mismatch"))
    if reason:
        reason="\n".join(reason)
        frappe.new_doc("Notification Log",
                       for_user=expense_doc.owner,
                       type="Alert",
                       document_type=expense_doc.doctype,
                       document_name=expense_doc.name,
                       subject="Your Expenses Ticket creation failed",
                       email_content=f"""Ticket creation failed by the Following reasons:{reason}"""
        ).insert(ignore_permissions=True)
        expense_doc.current_status="Declined"
        expense_doc.save()
        frappe.db.commit()
    else:
        approval_doc=frappe.new_doc("Approval")
        approval_doc.expense=expense_doc.name
        approval_doc.stage,approval_doc.approver=get_approver(expense_doc.name)
        approval_doc.save()
        approval_doc.submit()
        frappe.msgprint(f"Approvel request send to {approval_doc.stage}")

	
def get_approver(Expense):
        self=frappe.get_doc("Expense",Expense)
        team=frappe.get_value("Team Members",{"employee_id":self.employee_id,"parenttype":"Team"},"parent")
        if team:
            team_lead=frappe.get_value("Team",team,"team_lead")
            emp_id=frappe.get_value("Team Lead",team_lead,"lead_id")
            self.team_lead=emp_id
            self.save()
            return ("Team Lead",emp_id)
        else:
            manager=frappe.get_value("Employee",self.employee_id,"manager")
            return ("Manager",manager)

  
def get_receipt_data(image_path,values=None):
    from groq import Groq

    site_path = frappe.get_site_path()
    # If image_path starts with '/', os.path.join will ignore site_path.
    # Normalize leading slash so file URLs like /private/files/x.jpg are resolved under site.
    if not os.path.isabs(image_path):
        image_path = os.path.join(site_path, image_path)
    elif not image_path.startswith(site_path):
        image_path = os.path.join(site_path, image_path.lstrip("/"))
    # Getting the base64 string
    print(image_path)
    base64_image = encode_image(image_path)
    mime_type = mimetypes.guess_type(image_path)[0] or "image/jpeg"
    client = Groq(api_key=frappe.conf.get("ocr_api"))
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": [
                                        {"type": "text", "text": f"""Analyze this receipt image and compare it with the expected expense data.

Return exactly one valid JSON object and nothing else.

Schema:
{{
    "is_match": true | false,
    "reason": "short one-line reason"
}}

Rules:
- Set "is_match" to true only if the receipt matches the expected expense type, date, and amount.
- If any field is missing, mismatched, unreadable, or inconsistent, set "is_match" to false.
- Keep "reason" brief and specific.
- Do not add markdown, code fences, comments, or extra text.

Expected expense values:
- expense_type: {values['expense_type']}
- other_expense: {values['other_expense']}
- date_of_spending: {values['date_of_spending']}
- amount: {values['amount']}
- receipt: {values['receipt']}

Example valid response:
{{"is_match": false, "reason": "Amount on receipt does not match expected amount."}}"""},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:{mime_type};base64,{base64_image}",
                        },
                    },
                ],
            }
        ],
        model="qwen/qwen3.6-27b",
         stream=False,
    response_format={"type": "json_object"}
    
    )

    return json.loads(chat_completion.choices[0].message.content)

# Function to encode the image
def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')
