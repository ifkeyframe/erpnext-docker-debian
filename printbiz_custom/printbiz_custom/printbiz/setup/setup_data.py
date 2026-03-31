"""
PrintBiz — Seed data for Stage 1 (Warehouse Management)

Creates:
- Item Groups (categories)
- UOMs
- Warehouses
- Demo Items (blanks, consumables, packaging)

All functions are idempotent — safe to run multiple times.
"""

import frappe
from frappe import _


def setup_all():
    """Run all setup steps in order."""
    print("[SETUP] Starting PrintBiz seed data setup...")
    setup_uoms()
    setup_item_groups()
    setup_warehouses()
    setup_demo_items()
    frappe.db.commit()
    print("[SETUP OK] All seed data created successfully!")


def setup_uoms():
    """Create custom UOMs if they don't exist."""
    print("[SETUP] Creating UOMs...")
    uoms = [
        {"uom_name": "pcs", "must_be_whole_number": 1},
        {"uom_name": "meter", "must_be_whole_number": 0},
        {"uom_name": "sheet", "must_be_whole_number": 1},
        {"uom_name": "pack", "must_be_whole_number": 1},
        {"uom_name": "ml", "must_be_whole_number": 0},
    ]
    for uom_data in uoms:
        if not frappe.db.exists("UOM", uom_data["uom_name"]):
            doc = frappe.get_doc({"doctype": "UOM", **uom_data})
            doc.insert(ignore_permissions=True)
            print(f"  [OK] UOM created: {uom_data['uom_name']}")
        else:
            print(f"  [SKIP] UOM already exists: {uom_data['uom_name']}")


def setup_item_groups():
    """Create item group hierarchy."""
    print("[SETUP] Creating Item Groups...")
    groups = [
        {"item_group_name": "Blank Apparel", "parent_item_group": "All Item Groups"},
        {"item_group_name": "T-Shirts", "parent_item_group": "Blank Apparel"},
        {"item_group_name": "Hoodies", "parent_item_group": "Blank Apparel"},
        {"item_group_name": "Consumables", "parent_item_group": "All Item Groups"},
        {"item_group_name": "DTF Supplies", "parent_item_group": "Consumables"},
        {"item_group_name": "Packaging", "parent_item_group": "All Item Groups"},
        {"item_group_name": "Finished Goods", "parent_item_group": "All Item Groups"},
    ]
    for group_data in groups:
        if not frappe.db.exists("Item Group", group_data["item_group_name"]):
            doc = frappe.get_doc({"doctype": "Item Group", **group_data})
            doc.insert(ignore_permissions=True)
            print(f"  [OK] Item Group created: {group_data['item_group_name']}")
        else:
            print(f"  [SKIP] Item Group already exists: {group_data['item_group_name']}")


def setup_warehouses():
    """Create warehouses."""
    print("[SETUP] Creating Warehouses...")
    company = frappe.defaults.get_defaults().get("company", "PrintBiz")
    warehouses = [
        {
            "warehouse_name": "Main Warehouse",
            "company": company,
            "warehouse_type": "Warehouse",
        },
        {
            "warehouse_name": "Production Warehouse",
            "company": company,
            "warehouse_type": "Warehouse",
        },
    ]
    for wh_data in warehouses:
        full_name = f"{wh_data['warehouse_name']} - {frappe.get_cached_value('Company', company, 'abbr') or 'PB'}"
        if not frappe.db.exists("Warehouse", full_name):
            doc = frappe.get_doc({"doctype": "Warehouse", **wh_data})
            doc.insert(ignore_permissions=True)
            print(f"  [OK] Warehouse created: {full_name}")
        else:
            print(f"  [SKIP] Warehouse already exists: {full_name}")


def setup_demo_items():
    """Create demo items for testing."""
    print("[SETUP] Creating demo items...")
    company = frappe.defaults.get_defaults().get("company", "PrintBiz")
    abbr = frappe.get_cached_value("Company", company, "abbr") or "PB"
    default_warehouse = f"Main Warehouse - {abbr}"

    items = [
        # Blanks (t-shirts)
        {
            "item_code": "BLANK-TS-WH-S",
            "item_name": "T-Shirt White S",
            "item_group": "T-Shirts",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "custom_product_type": "Blank",
            "custom_color": "White",
            "custom_size": "S",
            "custom_is_blank": 1,
        },
        {
            "item_code": "BLANK-TS-WH-M",
            "item_name": "T-Shirt White M",
            "item_group": "T-Shirts",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "custom_product_type": "Blank",
            "custom_color": "White",
            "custom_size": "M",
            "custom_is_blank": 1,
        },
        {
            "item_code": "BLANK-TS-WH-L",
            "item_name": "T-Shirt White L",
            "item_group": "T-Shirts",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "custom_product_type": "Blank",
            "custom_color": "White",
            "custom_size": "L",
            "custom_is_blank": 1,
        },
        {
            "item_code": "BLANK-TS-BK-S",
            "item_name": "T-Shirt Black S",
            "item_group": "T-Shirts",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "custom_product_type": "Blank",
            "custom_color": "Black",
            "custom_size": "S",
            "custom_is_blank": 1,
        },
        {
            "item_code": "BLANK-TS-BK-M",
            "item_name": "T-Shirt Black M",
            "item_group": "T-Shirts",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "custom_product_type": "Blank",
            "custom_color": "Black",
            "custom_size": "M",
            "custom_is_blank": 1,
        },
        # Consumables
        {
            "item_code": "CONS-DTF-FILM",
            "item_name": "DTF Film",
            "item_group": "DTF Supplies",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "custom_product_type": "Consumable",
            "custom_is_consumable": 1,
        },
        {
            "item_code": "CONS-DTF-INK-BK",
            "item_name": "DTF Ink Black",
            "item_group": "DTF Supplies",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "custom_product_type": "Consumable",
            "custom_color": "Black",
            "custom_is_consumable": 1,
        },
        {
            "item_code": "CONS-DTF-INK-WH",
            "item_name": "DTF Ink White",
            "item_group": "DTF Supplies",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "custom_product_type": "Consumable",
            "custom_color": "White",
            "custom_is_consumable": 1,
        },
        # Packaging
        {
            "item_code": "PKG-POLYMAILER-M",
            "item_name": "Polymailer M",
            "item_group": "Packaging",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "custom_product_type": "Consumable",
            "custom_size": "M",
            "custom_is_consumable": 1,
        },
        {
            "item_code": "PKG-TAG-BRAND",
            "item_name": "Brand Tag",
            "item_group": "Packaging",
            "stock_uom": "Nos",
            "is_stock_item": 1,
            "custom_product_type": "Consumable",
            "custom_is_consumable": 1,
        },
    ]

    for item_data in items:
        if not frappe.db.exists("Item", item_data["item_code"]):
            # Separate custom fields from standard fields
            custom_fields = {}
            standard_fields = {}
            for key, value in item_data.items():
                if key.startswith("custom_"):
                    custom_fields[key] = value
                else:
                    standard_fields[key] = value

            doc = frappe.get_doc({"doctype": "Item", **standard_fields})

            # Set custom fields after doc creation
            for key, value in custom_fields.items():
                doc.set(key, value)

            doc.insert(ignore_permissions=True)
            print(f"  [OK] Item created: {item_data['item_code']} — {item_data['item_name']}")
        else:
            print(f"  [SKIP] Item already exists: {item_data['item_code']}")
