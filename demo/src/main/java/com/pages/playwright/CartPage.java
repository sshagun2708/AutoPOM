package com.pages.playwright;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;

public class CartPage {
    private final Page page;
    private final Locator cartPageTitle;
    private final Locator shoppingCartHeadIndicator;

    /**
     * Constructor for CartPage.
     * 
     * @param page Playwright Page instance
     */
    public CartPage(Page page) {
        this.page = page;
        this.cartPageTitle = page.locator("title");
        this.shoppingCartHeadIndicator = page.locator("#sc-head-end");
    }

    /**
     * Retrieves the text content of the page title element.
     * 
     * @return String text of the title locator
     */
    public String getCartPageTitleText() {
        return this.cartPageTitle.textContent();
    }

    /**
     * Standard Playwright page title retriever.
     * 
     * @return String HTML title of the page
     */
    public String getPageTitle() {
        return this.page.title();
    }

    /**
     * Checks if the shopping cart head indicator is visible on the page.
     * 
     * @return boolean true if visible, false otherwise
     */
    public boolean isShoppingCartHeadIndicatorVisible() {
        return this.shoppingCartHeadIndicator.isVisible();
    }

    /**
     * Waits for the shopping cart head indicator element to be visible.
     */
    public void waitForShoppingCartHeadIndicator() {
        this.shoppingCartHeadIndicator.waitFor();
    }
}