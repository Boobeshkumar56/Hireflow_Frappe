frappe.pages["hireflow-dashboard"].on_page_load = function (wrapper) {
	const page = frappe.ui.make_app_page({
		parent: wrapper,
		title: __("HireFlow"),
		single_column: true,
	});

	page.set_title(__("HireFlow"));
	const app = new HireflowAppShell(wrapper);
	app.render();
};

class HireflowAppShell {
	constructor(wrapper) {
		this.wrapper = $(wrapper);
		this.page = wrapper.page;
		this.modules = [
			{ label: "Employees", doctype: "Employee", icon: "users", accent: "#2563eb" },
			{ label: "Managers", doctype: "Manager", icon: "briefcase", accent: "#7c3aed" },
			{ label: "Expenses", doctype: "Expense", icon: "indian-rupee", accent: "#10b981" },
			{ label: "Approvals", doctype: "Approval", icon: "check-circle", accent: "#f59e0b" },
			{ label: "Finance Tickets", doctype: "Finance Ticket", icon: "ticket", accent: "#ef4444" },
			{ label: "Teams", doctype: "Team", icon: "build", accent: "#14b8a6" },
			{ label: "Team Leads", doctype: "Team Lead", icon: "command", accent: "#8b5cf6" },
		];
	}

	render() {
		this.load_module_data();
	}

	async load_module_data() {
		let total_records = 0;
		const module_data = [];

		for (const module of this.modules) {
			const [count, recent] = await Promise.all([
				frappe.db.count(module.doctype),
				frappe.db.get_list(module.doctype, {
					fields: ["name"],
					limit: 4,
					order_by: "creation desc",
				}),
			]);

			total_records += count || 0;
			module_data.push({
				...module,
				count: count || 0,
				recent: recent || [],
			});
		}

		this.render_shell(module_data, total_records);
	}

	render_shell(module_data, total_records) {
		const summary_cards = [
			{ label: "Total Records", value: total_records, accent: "#2563eb" },
			{ label: "Expense Claims", value: module_data.find((m) => m.doctype === "Expense")?.count || 0, accent: "#10b981" },
			{ label: "Approvals", value: module_data.find((m) => m.doctype === "Approval")?.count || 0, accent: "#f59e0b" },
		];

		const summary_html = summary_cards
			.map(
				(item) => `
				<div class="hireflow-summary-card">
					<div class="hireflow-summary-dot" style="background:${item.accent};"></div>
					<div>
						<div class="hireflow-summary-label">${item.label}</div>
						<div class="hireflow-summary-value">${item.value}</div>
					</div>
				</div>
			`
			)
			.join("");

		const cards_html = module_data
			.map((module) => {
				let recent_items = `<div class="hireflow-empty-state">${__("No records created yet")}</div>`;
				if (module.recent.length) {
					recent_items = module.recent
						.map(
							(doc) => `
								<div class="hireflow-row-item">
									<span>${doc.name}</span>
									<button class="btn btn-default btn-xs hireflow-open-btn" data-route="Form" data-doctype="${module.doctype}" data-name="${doc.name}">
										${__("Open")}
									</button>
								</div>
							`
						)
						.join("");
				}

				return `
					<div class="hireflow-module-card">
						<div class="hireflow-module-head">
							<div class="hireflow-title-wrap">
								<div class="hireflow-icon" style="background:${module.accent};">
									${frappe.utils.icon(module.icon)}
								</div>
								<div>
									<h3>${module.label}</h3>
									<p>${module.count} ${__("records")}</p>
								</div>
							</div>
							<div class="hireflow-actions">
								<button class="btn btn-primary btn-sm hireflow-open-btn" data-route="List" data-doctype="${module.doctype}">${__("Open List")}</button>
								<button class="btn btn-default btn-sm hireflow-open-btn" data-route="new" data-doctype="${module.doctype}">${__("New")}</button>
							</div>
						</div>
						<div class="hireflow-record-list">${recent_items}</div>
					</div>
				`;
			})
			.join("");

		$(this.page.body).html(`
			<style>
				.hireflow-shell {
					padding: 1rem;
					background: linear-gradient(180deg, #f8fbff 0%, #eef3fb 100%);
					border-radius: 24px;
				}
				.hireflow-topbar {
					display: flex;
					justify-content: space-between;
					align-items: center;
					gap: 1rem;
					margin-bottom: 1.25rem;
					padding: 1.1rem 1.2rem;
					background: rgba(255,255,255,0.9);
					border: 1px solid rgba(148,163,184,0.2);
					border-radius: 18px;
					box-shadow: 0 8px 24px rgba(15,23,42,0.04);
				}
				.hireflow-topbar h2 {
					margin: 0;
					font-size: 1.6rem;
					font-weight: 800;
					color: #0f172a;
				}
				.hireflow-badge {
					display: inline-flex;
					padding: 0.35rem 0.7rem;
					border-radius: 999px;
					background: rgba(37,99,235,0.08);
					color: #1d4ed8;
					font-size: 0.76rem;
					font-weight: 700;
					letter-spacing: 0.04em;
					text-transform: uppercase;
				}
				.hireflow-summary-grid {
					display: grid;
					grid-template-columns: repeat(3, minmax(0, 1fr));
					gap: 1rem;
					margin-bottom: 1.25rem;
				}
				.hireflow-summary-card {
					display: flex;
					align-items: center;
					gap: 0.9rem;
					padding: 1rem 1.1rem;
					background: rgba(255,255,255,0.9);
					border: 1px solid rgba(148,163,184,0.2);
					border-radius: 18px;
					box-shadow: 0 8px 20px rgba(15,23,42,0.03);
				}
				.hireflow-summary-dot {
					width: 12px;
					height: 12px;
					border-radius: 999px;
				}
				.hireflow-summary-label {
					font-size: 0.78rem;
					color: #64748b;
					text-transform: uppercase;
					letter-spacing: 0.06em;
				}
				.hireflow-summary-value {
					font-size: 1.8rem;
					font-weight: 800;
					color: #0f172a;
					line-height: 1.1;
				}
				.hireflow-module-grid {
					display: grid;
					grid-template-columns: repeat(2, minmax(0, 1fr));
					gap: 1rem;
				}
				.hireflow-module-card {
					padding: 1rem;
					background: rgba(255,255,255,0.94);
					border: 1px solid rgba(148,163,184,0.18);
					border-radius: 18px;
					box-shadow: 0 10px 22px rgba(15,23,42,0.04);
				}
				.hireflow-module-head {
					display: flex;
					justify-content: space-between;
					align-items: center;
					gap: 1rem;
					margin-bottom: 0.9rem;
				}
				.hireflow-title-wrap {
					display: flex;
					align-items: center;
					gap: 0.8rem;
				}
				.hireflow-icon {
					display: inline-flex;
					align-items: center;
					justify-content: center;
					width: 2.4rem;
					height: 2.4rem;
					border-radius: 12px;
					color: white;
					font-size: 1rem;
				}
				.hireflow-module-head h3 {
					margin: 0;
					font-size: 1.05rem;
					font-weight: 700;
					color: #0f172a;
				}
				.hireflow-module-head p {
					margin: 0.2rem 0 0;
					font-size: 0.84rem;
					color: #64748b;
				}
				.hireflow-actions {
					display: flex;
					gap: 0.5rem;
					flex-wrap: wrap;
				}
				.hireflow-record-list {
					display: grid;
					gap: 0.55rem;
				}
				.hireflow-row-item {
					display: flex;
					justify-content: space-between;
					align-items: center;
					gap: 0.6rem;
					padding: 0.6rem 0.75rem;
					border-radius: 10px;
					background: #f8fafc;
					border: 1px solid rgba(148,163,184,0.12);
					color: #0f172a;
					font-size: 0.92rem;
				}
				.hireflow-empty-state {
					padding: 0.75rem;
					border-radius: 10px;
					background: #f8fafc;
					color: #64748b;
					font-size: 0.9rem;
				}
				@media (max-width: 900px) {
					.hireflow-summary-grid,
					.hireflow-module-grid {
						grid-template-columns: 1fr;
					}
					.hireflow-topbar,
					.hireflow-module-head {
						flex-direction: column;
						align-items: flex-start;
					}
				}
			</style>
			<div class="hireflow-shell">
				<div class="hireflow-topbar">
					<h2>${__("HireFlow Workspace")}</h2>
					<span class="hireflow-badge">${__("Operations")}</span>
				</div>
				<div class="hireflow-summary-grid">${summary_html}</div>
				<div class="hireflow-module-grid">${cards_html}</div>
			</div>
		`);

		this.bind_actions();
	}

	bind_actions() {
		this.page.body.find(".hireflow-open-btn").on("click", function () {
			const route = $(this).data("route");
			const doctype = $(this).data("doctype");
			const name = $(this).data("name");

			if (route === "new") {
				frappe.new_doc(doctype);
				return;
			}

			if (name) {
				frappe.set_route(route, doctype, name);
				return;
			}

			frappe.set_route(route, doctype);
		});
	}
}
