package com.pages.playwright;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;

/**
 * Page Object Model representing the Product Details Page.
 */
public class ProductDetailsPage {

    private final Page page;
    private final Locator productTitle;
    private final Locator addToCartButton;
    private final Locator cartButton;
    private final Locator cartCountIndicator;

    /**
     * Constructor for ProductDetailsPage.
     *
     * @param page the Playwright Page instance
     */
    public ProductDetailsPage(Page page) {
        this.page = page;
        this.productTitle = page.locator("#productTitle");
        this.addToCartButton = page.locator("#add-to-cart-button");
        this.cartButton = page.locator("#nav-cart");
        this.cartCountIndicator = page.locator("#nav-cart-count");
    }

    /**
     * Gets the text of the product title.
     *
     * @return the product title text
     */
    public String getProductTitleText() {
        return this.productTitle.textContent().trim();
    }

    /**
     * Clicks the "Add to Cart" button.
     */
    public void clickAddToCart() {
        this.addToCartButton.click();
    }

    /**
     * Clicks the cart button to navigate to the cart page.
     */
    public void clickCart() {
        this.cartButton.click();
    }

    /**
     * Gets the current cart count text indicator.
     *
     * @return the text value of the cart count (e.g., "1", "2")
     */
    public String getCartCountText() {
        return this.cartCountIndicator.textContent().trim();
    }

    /**
     * Gets the current cart count as an integer.
     *
     * @return the cart count as an integer, or 0 if parsing fails
     */
    public int getCartCount() {
        String countText = getCartCountText();
        try {
            return countText.isEmpty() ? 0 : Integer.parseInt(countText);
        } catch (NumberFormatException e) {
            return 0;
        }
    }

    /**
     * Checks if the product title is visible.
     *
     * @return true if visible, false otherwise
     */
    public boolean isProductTitleVisible() {
        return this.productTitle.isVisible();
    }
}