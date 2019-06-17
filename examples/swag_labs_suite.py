import pytest
from parameterized import parameterized
from seleniumbase import BaseCase


class SwagLabsTests(BaseCase):

    def login(self, user="standard_user"):
        """ Login to Swag Labs and assert that the login was successful. """
        if user not in (["standard_user", "problem_user"]):
            raise Exception("Invalid user!")
        self.open("https://www.saucedemo.com/")
        self.update_text("#user-name", user)
        self.update_text("#password", "secret_sauce")
        self.click('input[type="submit"]')
        self.assert_text("Products", "div.product_label")
        self.assert_element("#inventory_container")

    @parameterized.expand([
        ["standard_user"],
        ["problem_user"],
    ])
    @pytest.mark.run(order=1)
    def test_swag_labs_basic_functional_flow(self, user):
        """ This test checks for basic functional flow in the Swag Labs store.
            The test is parameterized, and receives the user to use for login.
        """
        self.login(user)

        # Verify that the "Test.allTheThings() T-Shirt" appears on the page
        item_name = "Test.allTheThings() T-Shirt"
        self.assert_text(item_name)

        # Verify that a reverse-alphabetical sort works as expected
        self.select_option_by_value("select.product_sort_container", "za")
        if item_name not in self.get_text("div.inventory_item"):
            raise Exception('Sort Failed! Expecting "%s" on top!' % item_name)

        # Add the "Test.allTheThings() T-Shirt" to the cart
        self.assert_exact_text("ADD TO CART", "button.btn_inventory")
        item_price = self.get_text("div.inventory_item_price")
        self.click("button.btn_inventory")
        self.assert_exact_text("REMOVE", "button.btn_inventory")
        self.assert_exact_text("1", "span.shopping_cart_badge")

        # Verify your cart
        self.click("#shopping_cart_container path")
        self.assert_exact_text("Your Cart", "div.subheader")
        self.assert_text(item_name, "div.inventory_item_name")
        self.assert_exact_text("1", "div.cart_quantity")
        self.assert_exact_text("REMOVE", "button.cart_button")
        self.assert_element("link=CONTINUE SHOPPING")

        # Checkout - Add info
        self.click("link=CHECKOUT")
        self.assert_exact_text("Checkout: Your Information", "div.subheader")
        self.assert_element("a.cart_cancel_link")
        self.update_text("#first-name", "SeleniumBase")
        self.update_text("#last-name", "Rocks")
        self.update_text("#postal-code", "01720")

        # Checkout - Overview
        self.click("input.btn_primary")
        self.assert_exact_text("Checkout: Overview", "div.subheader")
        self.assert_element("link=CANCEL")
        self.assert_text(item_name, "div.inventory_item_name")
        self.assert_text(item_price, "div.inventory_item_price")
        self.assert_exact_text("1", "div.summary_quantity")

        # Finish Checkout and verify item is no longer in cart
        self.click("link=FINISH")
        self.assert_exact_text("THANK YOU FOR YOUR ORDER", "h2")
        self.assert_element("div.pony_express")
        self.click("#shopping_cart_container path")
        self.assert_element_absent("div.inventory_item_name")
        self.click("link=CONTINUE SHOPPING")
        self.assert_element_absent("span.shopping_cart_badge")

    @parameterized.expand([
        ["standard_user"],
        ["problem_user"],
    ])
    @pytest.mark.run(order=2)
    def test_swag_labs_products_page_resource_verification(self, user):
        """ This test checks for 404 errors on the Swag Labs products page.
            The test is parameterized, and receives the user to use for login.
        """
        self.login(user)
        self.assert_no_404_errors()
