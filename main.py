import flet as ft
from flet import colors
from pymongo import MongoClient
from bson import ObjectId
import threading 

def main(page: ft.Page):
    page.title = "FCA App"
    page.bgcolor = colors.BLACK

    client = MongoClient("mongodb+srv://moiz121:test123456@cluster0.lq8grwq.mongodb.net/")  
    db = client["UserAuthDB"]
    users_collection = db["Users"]

    navigation_stack = []

    def show_message(message, success=True):
        page.snack_bar = ft.SnackBar(
            content=ft.Text(message),
            bgcolor=colors.GREEN if success else colors.RED
        )
        page.snack_bar.open = True
        page.update()

    def navigate_to(route, clear_history=False):
        if clear_history:
            navigation_stack.clear()
        navigation_stack.append(route)
        route_change(route)

    def go_back(e):
        if len(navigation_stack) > 1:
            navigation_stack.pop()
            previous_route = navigation_stack[-1]
            route_change(previous_route)
        else:
            show_message("You're already at the main page", success=False)

    def route_change(route):
        page.controls.clear()
        
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.scroll = None

        if route == "/":
            load_main_page()
        elif route == "/login":
            load_Login_page()
        elif route == "/signup":
            load_Signup_page()
        elif route == "/handbook":
            load_handbook_viewer()
        page.update()

    def handle_login(e):
        username = username_field.value.strip()
        password = password_field.value.strip()

        if not username or not password:
            show_message("Username and password cannot be empty!", success=False)
        else:
            user = users_collection.find_one({"username": username})
            if user and user["password"] == password:
                show_message("Login successful!", success=True)
                page.controls.clear()
                pr = ft.ProgressRing()

                page.add(
                    ft.Row(
                        [
                            pr,
                            ft.Text("Wait for the completion...", size=16, weight="bold", color="WHITE")
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=10,
                    )
                )
                page.update()
                navigate_to("/handbook")
            else:
                show_message("Invalid username or password.", success=False)

    def handle_signup(e):
        username = signup_username_field.value.strip()
        password = signup_password_field.value.strip()
        confirm_password = signup_confirm_password_field.value.strip()

        if not username or not password or not confirm_password:
            show_message("All fields must be filled out!", success=False)
        elif password != confirm_password:
            show_message("Passwords do not match.", success=False)
        else:
            if users_collection.find_one({"username": username}):
                show_message("Username already exists.", success=False)
            else:
                users_collection.insert_one({"username": username, "password": password})
                show_message("Signup successful!", success=True)
                navigate_to("/login")

    def load_Login_page():
        global username_field, password_field

        username_field = ft.TextField(label="Username", color="white", autofocus=True, border_color=colors.YELLOW, border_radius=28)
        password_field = ft.TextField(label="Password", color="white", border_color=colors.YELLOW, password=True, can_reveal_password=True, border_radius=28)

        page.add(
            ft.Column(
                [
                    ft.Image(
                        src="https://cdn-icons-png.flaticon.com/128/295/295128.png",
                        width=100,
                        height=100,
                        fit=ft.ImageFit.COVER
                    ),
                    ft.Text("LOGIN", size=30, weight="bold", text_align="center", color="WHITE"),
                    username_field,
                    password_field,
                    ft.ElevatedButton(text="Log In", bgcolor=colors.YELLOW, color=colors.BLACK, on_click=handle_login, width=500),
                    ft.Text("Don't have an account?", size=12, weight="bold", text_align="center", color="WHITE"),
                    ft.ElevatedButton(text="Sign Up", bgcolor=colors.GREEN, color=colors.WHITE, on_click=lambda _: navigate_to("/signup"), width=300),
                    ft.ElevatedButton(text="Back to Main", bgcolor=colors.RED, color=colors.WHITE, on_click=lambda _: navigate_to("/"))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )

    def load_Signup_page():
        global signup_username_field, signup_password_field, signup_confirm_password_field

        signup_username_field = ft.TextField(label="Username", color="white", autofocus=True, border_color=colors.YELLOW, border_radius=28)
        signup_password_field = ft.TextField(label="Password", color="white", border_color=colors.YELLOW, password=True, can_reveal_password=True, border_radius=28)
        signup_confirm_password_field = ft.TextField(label="Confirm Password", color="white", border_color=colors.YELLOW, password=True, can_reveal_password=True, border_radius=28)

        page.add(
            ft.Column(
                [
                    ft.Image(
                        src="https://cdn-icons-png.flaticon.com/128/15753/15753940.png",
                        width=90,
                        height=90,
                        fit=ft.ImageFit.COVER
                    ),
                    ft.Text("SIGNUP", size=30, weight="bold", text_align="center", color="WHITE"),
                    signup_username_field,
                    signup_password_field,
                    signup_confirm_password_field,
                    ft.ElevatedButton(text="Sign Up", bgcolor=colors.YELLOW, color=colors.BLACK, on_click=handle_signup, width=500),
                    ft.Text("Already have an account?", size=12, weight="bold", text_align="center", color="WHITE"),
                    ft.ElevatedButton(text="Back to Login", bgcolor=colors.RED, color=colors.WHITE, on_click=lambda _: navigate_to("/login"))
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=10,
            )
        )

    

    def load_handbook_viewer():
     page.bgcolor = ft.colors.BLACK
     page.padding = 20
     page.scroll = "auto"

    db = client['FCAHANDBOOK']

    high_level_standards = {
        "HIGH LEVEL STANDARDS": [
            {
                "name": "PRIN Principles for Businesses",
                "subsections": [
                    {
                        "name": "PRIN 1 Introduction",
                        "collections": [
                            {"name": "PRIN 1.1 Application and purpose", "collection": "PRIN1.1ApplicationandPurpose"},
                            {"name": "PRIN 1.2 Clients and the Principles", "collection": "PRIN1.2ClientsAndPrinciples"},
                            {"name": "PRIN 1 Annex 1", "collection": "PRIN1ANNEX1"}
                        ]
                    },
                    {
                        "name": "PRIN 2 The Principles",
                        "collections": [{"name": "PRIN 2.1 The Principles", "collection": "PRIN2.1ThePrinciples"}]
                    },
                    {
                        "name": "PRIN 2A The Consumer Duty",
                        "collections": [
                            {"name": "PRIN 2A.1 Application and purpose", "collection": "PRIN2A.1ApplicationandPurpose"},
                            {"name": "PRIN 2A.2 Cross-cutting obligations", "collection": "PRIN2A.2CrossCuttingObligations"},
                            {"name": "PRIN 2A.3 Consumer Duty: retail customer outcome - products and services", "collection": "PRIN2A.3productsandservices"},
                            {"name": "PRIN 2A.4 Consumer Duty: retail customer outcome on price and value", "collection": "PRIN2A.4priceandvalue"},
                            {"name": "PRIN 2A.5 Consumer Duty: retail customer outcome on consumer understanding", "collection": "PRIN2A.5outcomeonconsumerunderstanding"},
                            {"name": "PRIN 2A.6 Consumer Duty: retail customer outcome on consumer support", "collection": "PRIN2A.6outcomeonconsumersupport"},
                            {"name": "PRIN 2A.7 General", "collection": "PRIN2A.7General"},
                            {"name": "PRIN 2A.8 Governance and culture", "collection": "PRIN2A.8Governanceandculture"},
                            {"name": "PRIN 2A.9 Monitoring of consumer outcomes", "collection": "PRIN2A.9Monitoringofconsumeroutcomes"},
                            {"name": "PRIN 2A.10 Redress or other appropriate action", "collection": "PRIN2A.10Redressorotherappropriateaction"},
                            {"name": "PRIN 2A.11 Sale and purchase of product books", "collection": "PRIN2A.11Saleandpurchaseofproductbooks"}
                        ]
                    },
                    {
                        "name": "PRIN 3 Rules about application",
                        "collections": [
                            {"name": "PRIN 3.1 Who?", "collection": "PRIN3.1WHO"},
                            {"name": "PRIN 3.2 What?", "collection": "PRIN3.2WHAT"},
                            {"name": "PRIN 3.3 Where?", "collection": "PRIN3.3WHERE"},
                            {"name": "PRIN 3.4 General", "collection": "PRIN3.4GENERAL"}
                        ]
                    },
                    {
                        "name": "PRIN 4 Principles: MiFID business",
                        "collections": [
                            {"name": "PRIN 4.1 Principles: MiFID business", "collection": "PRIN4.1PrinciplesMiFIDbusiness"},
                            {"name": "PRIN TP 1 Transitional provisions", "collection": "PRINTPTransitionalprovisions"},
                            {"name": "PRIN Sch 2 Notification requirements", "collection": "PRINSch2Notificationrequirements"},
                            {"name": "PRIN Sch 5 Rights of action for damages", "collection": "PRINSch5Rightsofactionfordamages"},
                            {"name": "PRIN Sch 6 Rules that can be waived", "collection": "PRINSch6Rulesthatcanbewaived"}
                        ]
                    }
                ]
            }
        ]
    }

    def fetch_handbook_data(collection_name):
        collection = db[collection_name]
        return list(collection.find())

    def show_details(e):
        collection_name, item_id = e.control.data
        collection = db[collection_name]
        item = collection.find_one({'_id': ObjectId(item_id)})
        
        if item is None:
            details_view.controls = [ft.Text("Item not found", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE)]
        else:
            if collection_name == "PRINTPTransitionalprovisions":
                details_view.controls = [
                    ft.Text(item.get('Section', 'No Section Available'), size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Text(f"Material to which the transitional provision applies: {item.get('Material to which the transitional provision applies', 'Not Available')}", size=16, color=ft.colors.WHITE),
                    ft.Text(f"Transitional Provision: {item.get('Transitional Provision', 'Not Available')}", size=16, color=ft.colors.WHITE),
                    ft.Text(f"Transitional Provision: dates in force: {item.get('Transitional Provision: dates in force', 'Not Available')}", size=16, color=ft.colors.WHITE),
                    ft.Text(f"Handbook provision: coming into force: {item.get('Handbook provision: coming into force', 'Not Available')}", size=16, color=ft.colors.WHITE),
                    ft.ElevatedButton("Back to List", on_click=lambda _: switch_view("list"), style=ft.ButtonStyle(color=ft.colors.WHITE,bgcolor=ft.colors.YELLOW,))
                ]
            else:
                details_view.controls = [
                    ft.Text(item.get('Section', 'No Section Available'), size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Text(f"ID: {item.get('ID', 'No ID Available')}", size=16, color=ft.colors.WHITE),
                    ft.Text(f"Dated: {item.get('Dated', 'No Date Available')}", size=16, color=ft.colors.WHITE),
                    ft.Text("Description:", size=18, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
                    ft.Text(item.get('Description', 'No Description Available'), size=16, color=ft.colors.WHITE),
                    ft.Container(
                        content=ft.TextButton(
                            "Back to List",
                            on_click=lambda _: switch_view("list"),
                            style=ft.ButtonStyle(color=ft.colors.BLACK),
                        ),
                        bgcolor=ft.colors.YELLOW_ACCENT,
                        border_radius=22,
                        padding=5,
                    )
                ]
        switch_view("details")

    def switch_view(view):
        if view == "list":
            navigation_view.visible = True
            details_view.visible = False
        else:
            navigation_view.visible = False
            details_view.visible = True
        page.update()

    def toggle_section(e):
        section_content = e.control.data
        section_content.visible = not section_content.visible
        e.control.icon = ft.icons.EXPAND_LESS if section_content.visible else ft.icons.EXPAND_MORE
        page.update()

    navigation_view = ft.Column(scroll="auto", controls=[
        ft.Text("HIGH LEVEL STANDARDS", size=32, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
        ft.Divider(color=ft.colors.WHITE),
    ])

    for main_section in high_level_standards["HIGH LEVEL STANDARDS"]:
        main_section_name = main_section["name"]
        main_section_items = ft.Column(visible=False)

        for subsection in main_section["subsections"]:
            subsection_name = subsection["name"]
            subsection_items = ft.Column(visible=False)

            for collection_info in subsection["collections"]:
                collection_name = collection_info["name"]
                collection_data = collection_info["collection"]
                
                collection_items = ft.Column()
                for item in fetch_handbook_data(collection_data):
                    if collection_data == "PRINTPTransitionalprovisions":
                        subtitle_text = f"{item.get('Material to which the transitional provision applies', 'Not Available')[:100]}..."
                    else:
                        subtitle_text = f"{item.get('ID', 'No ID Available')} - {item.get('Description', 'No Description Available')[:100]}..."
                    
                    collection_items.controls.append(
                        ft.ListTile(
                            title=ft.Text(item.get('Section', 'No Section Available'), color=ft.colors.WHITE),
                            subtitle=ft.Text(subtitle_text, color=ft.colors.WHITE70),
                            on_click=show_details,
                            data=(collection_data, str(item['_id']))
                        )
                    )

                collection_header = ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(collection_name, color=ft.colors.WHITE, expand=True),
                            ft.IconButton(
                                icon=ft.icons.EXPAND_MORE,
                                icon_color=ft.colors.WHITE,
                                on_click=toggle_section,
                                data=collection_items,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    ),
                    bgcolor=ft.colors.BLUE_GREY_900,
                    padding=10,
                    border_radius=5,
                )
                subsection_items.controls.extend([collection_header, collection_items])

            subsection_header = ft.Container(
                content=ft.Row(
                    [
                        ft.Text(subsection_name, color=ft.colors.WHITE, expand=True),
                        ft.IconButton(
                            icon=ft.icons.EXPAND_MORE,
                            icon_color=ft.colors.WHITE,
                            on_click=toggle_section,
                            data=subsection_items,
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
                bgcolor=ft.colors.BLUE_GREY_800,
                padding=10,
                border_radius=5,
            )
            main_section_items.controls.extend([subsection_header, subsection_items])

        main_section_header = ft.Container(
            content=ft.Row(
                [
                    ft.Text(main_section_name, color=ft.colors.WHITE, expand=True),
                    ft.IconButton(
                        icon=ft.icons.EXPAND_MORE,
                        icon_color=ft.colors.WHITE,
                        on_click=toggle_section,
                        data=main_section_items,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=ft.colors.BLUE_GREY_700,
            padding=10,
            border_radius=5,
        )
        navigation_view.controls.extend([main_section_header, main_section_items])

    details_view = ft.Column(visible=False)

    content = ft.Column(
        controls=[
            ft.Row([
                ft.IconButton(ft.icons.ARROW_BACK, icon_size = 24, on_click=go_back),
                ft.Icon(ft.icons.MENU_BOOK, color=ft.colors.YELLOW, size=40),
                ft.Text("FCA Handbook Viewer", size=20, weight=ft.FontWeight.BOLD, color=ft.colors.WHITE),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Container(height=20),
            navigation_view,
            details_view
        ],
        scroll="auto",
        expand=True
    )

    page.add(content)

    switch_view("list")

    def load_main_page():
        page.add(
            ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Image(
                                    src="https://tradingguide.co.uk/wp-content/uploads/2023/06/What-is-the-Financial-Conduct-Authority-FCA.png",
                                    width=200,
                                    height=100,
                                    fit=ft.ImageFit.COVER
                                ),
                                ft.Text(
                                    "We ensure fair and ethical financial markets, protecting consumers.",
                                    size=15,
                                    weight="bold",
                                    text_align="center",
                                    color="WHITE"
                                ),
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                            spacing=10,
                        ),
                        expand=True,
                    ),
                    ft.ElevatedButton(
                        text="GET STARTED",
                        bgcolor=colors.YELLOW,
                        color=colors.BLACK,
                        on_click=lambda _: navigate_to("/login"),
                        width=200,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
                expand=True,
            )
        )
        navigate_to("/", clear_history=True)
  
ft.app(target=main)