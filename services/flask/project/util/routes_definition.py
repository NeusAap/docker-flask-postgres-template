from flask import render_template


def get_all_website_routes():
    routes = {
        "Home": [
            {
                "url": "/home",
                "label": "Introduction",
                "show": True,
                "description": "Turning ideas into reality.",
            },
            {
                "url": "/services",
                "label": "Key services",
                "show": False,
                "description": "All services briefly explained.",
            },
        ],
        "Services": [
            {
                "url": "/services/software",
                "label": "Software Solutions",
                "show": True,
                "description": "Software solutions specifically made for you!",
            },
            {
                "url": "/services/product-development",
                "label": "Product Development",
                "show": True,
                "description": "End-to-end development of products, with your best ideas.",
            },
            {
                "url": "/services/infrastructure",
                "label": "Infrastructure",
                "show": True,
                "description": "Infrastructure to perfectly suit your needs.",
            },
        ],
        "Portfolio": [
            {
                "url": "/portfolio/motorsport-display",
                "label": "Digital Motorsport Display",
                "show": True,
                "description": "A digital CAN display for circuit or rally drivers.",
            },
            {
                "url": "/portfolio/shot-clock",
                "label": "Poker shot-clock",
                "show": True,
                "description": "Never miss your poker turn again!",
            },
            {
                "url": "/portfolio/project-a",
                "label": "Project A",
                "show": True,
                "description": "A fun car made with passion by enthousiasts.",
            },
            {
                "url": "/portfolio/card-shuffler",
                "label": "Card Shuffler",
                "show": True,
                "description": "An advanced card shuffler, capable of unfair play.",
            },
            {
                "url": "/portfolio/lawnmower-tuning",
                "label": "Lawnmower Tuning",
                "show": True,
                "description": "An old school lawnmower, with a modern touch.",
            },
        ],
        "Contact": [
            {
                "url": "/contact",
                "label": "Contact us",
                "show": True,
                "description": "Get in touch with us!",
            }
        ],
        "Authentication": [
            {
                "url": "/login",
                "label": "Login",
                "show": False,
                "description": "Login page.",
            },
            {
                "url": "/register",
                "label": "Register",
                "show": False,
                "description": "Register page.",
            },
        ],
    }

    return dict(routes=routes)


def get_subroute(sub_route_to_get: str):
    sub_route_to_get = sub_route_to_get.lower()
    sub_route_to_get = sub_route_to_get.capitalize()

    website_routes = get_all_website_routes()
    sub_route = website_routes.get("routes").get(sub_route_to_get)
    return sub_route


def get_subroute_urls(module_routes: list[dict[str, str]]):
    last_parts: list[str] = [route["url"].split("/")[-1] for route in module_routes]
    return last_parts


def get_subroute_labels(module_routes: list[dict[str, str]]):
    labels = [route["label"] for route in module_routes]
    return labels


def get_subroute_element_by_subroute_segment(
    module_routes: list[dict[str, str]], segment: str, element_name: str = "label"
):
    for route in module_routes:
        url_segment = route["url"].split("/")[-1]
        if url_segment == segment:
            try:
                return route[element_name]
            except KeyError:
                return None
    return None


def create_blueprint_views_dynamically(blueprint, module_name):
    # Define route handlers dynamically
    for subroute in blueprint.module_subroute_urls:

        def create_route_handler(subroute_segment):
            def route_display_func():
                label = get_subroute_element_by_subroute_segment(
                    module_routes=blueprint.module_routes,
                    segment=subroute_segment,
                    element_name="label",
                )
                description = get_subroute_element_by_subroute_segment(
                    module_routes=blueprint.module_routes,
                    segment=subroute_segment,
                    element_name="description",
                )

                template_name = f"{module_name}/{subroute_segment}.html"
                return render_template(
                    template_name,
                    segment=subroute_segment,
                    page_label=label,
                    page_description=description,
                )

            return route_display_func

        # Register the route with a unique endpoint
        blueprint.route(f"/{subroute}", endpoint=f"{subroute}_handler")(
            create_route_handler(subroute)
        )
