from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string

__version__ = "0.1.0"


class Menu:
    ROOT = "root"
    PLAIN = "plain"
    LINK = "link"
    TREE = "tree"

    def __init__(
        self, menu_type, text="", url="#", class_name="", icon="", **kwargs
    ):
        self.menu_type = menu_type
        self.text = text
        self.url = url
        self.class_name = class_name
        self.icon = icon
        self.attrs = kwargs.pop("attrs", {})
        self.menus = kwargs.pop("menus", [])
        self.kwargs = kwargs

        self.attrs = " ".join(
            "%s=%s" % (key, value) for key, value in self.attrs.items()
        )
        self.menus = (menu.render() for menu in self.menus)

    def render(self):
        """Render menu"""
        if self.menu_type == self.ROOT:
            return self.render_root()

        if self.menu_type == self.PLAIN:
            return self.render_plain()

        if self.menu_type == self.LINK:
            return self.render_link()

        if self.menu_type == self.TREE:
            return self.render_tree()

        raise ImproperlyConfigured(
            f"Menu type {self.menu_type} is invalid, options are: "
            f"{self.ROOT}, {self.PLAIN}, {self.LINK}, {self.TREE}"
        )

    def render_root(self):
        """Render "root" menu"""
        context = {
            "class_name": self.class_name,
            "attrs": self.attrs,
            "menus": self.menus,
        }
        return render_to_string("sidebar_menu/root.html", context)

    def render_plain(self):
        """Render "header" menu"""
        context = {"class_name": self.class_name, "text": self.text}
        return render_to_string("sidebar_menu/plain.html", context,)

    def render_link(self):
        """Render "link" menu"""
        context = {
            "active_class": "",
            "url": self.url,
            "text": self.text,
            **self.kwargs,
        }
        return render_to_string("sidebar_menu/link.html", context)

    def render_tree(self):
        """Render "tree" menu"""
        context = {
            "active_class": "",
            "text": self.text,
            "menus": self.menus,
            **self.kwargs,
        }
        return render_to_string("sidebar_menu/tree.html", context)
