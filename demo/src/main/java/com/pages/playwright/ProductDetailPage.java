package com.pages.playwright;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;

/**
 * Page Object Model representing the Product Detail Page.
 */
public class ProductDetailPage {
    private final Page page;
    private final Locator productTitle;
    private final Locator addToCartButton;
    private final Locator cartButton;
    private final Locator cartCountIndicator;

    /**
     * Constructor for ProductDetailPage.
     * 
     * @param page The Playwright Page instance.
     */
    public ProductDetailPage(Page page) {
        this.page = page;
        this.productTitle = page.locator("#productTitle");
        this.addToCartButton = page.locator("#add-to-cart-button");
        this.cartButton = page.locator("#nav-cart");
        this.cartCountIndicator = page.locator("#nav-cart-count");
    }

    /**
     * Gets the text of the product title.
     * 
     * @return The product title text.
     */
    public String getProductTitleText() {
        return this.productTitle.textContent().trim();
    }

    /**
     * Clicks the 'Add to Cart' button.
     */
    public void clickAddToCart() {
        this.addToCartButton.click();
    }

    /**
     * Clicks the Cart button to navigate to the cart page.
     */
    public void clickCart() {
        this.cartButton.click();
    }

    /**
     * Gets the current cart count from the cart indicator.
     * 
     * @return The cart count as a String.
     */
    public String getCartCount() {
        return this.cartCountIndicator.textContent().trim();
    }

    /**
     * Helper method to get the product title Locator for custom assertions.
     * 
     * @return The product title Locator.
     */
    public Locator getProductTitleLocator() {
        return this.productTitle;
    }

    /**
     * Helper method to get the cart count Locator for assertions.
     * 
     * @return The cart count Locator.
     */
    public Locator getCartCountLocator() {
        return this.cartCountIndicator;
    }
}