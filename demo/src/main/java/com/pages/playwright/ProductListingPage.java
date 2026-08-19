package com.pages.playwright;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;

/**
 * Page Object Model representing the Product Listing Page (PLP).
 */
public class ProductListingPage {

    private final Page page;
    
    // Playwright Locators
    private final Locator productCards;
    private final Locator productLinks;
    private final Locator productImages;

    /**
     * Constructor initializing the page and its associated locators.
     * 
     * @param page the Playwright Page instance
     */
    public ProductListingPage(Page page) {
        this.page = page;
        
        // Locators assigned using CSS selectors targeting non-sponsored search result items
        this.productCards = page.locator("div.s-result-item[data-component-type='s-search-result']:not(:has(.s-sponsored-label-info))");
        this.productLinks = page.locator("div.s-result-item[data-component-type='s-search-result']:not(:has(.s-sponsored-label-info)) h2 a.a-link-normal");
        this.productImages = page.locator("div.s-result-item[data-component-type='s-search-result'] img.s-image");
    }

    /**
     * Waits for the product cards to be visible on the page.
     */
    public void waitForPageToLoad() {
        this.productCards.first().waitFor();
    }

    /**
     * Retrieves the total count of non-sponsored product cards currently displayed.
     * 
     * @return count of product cards
     */
    public int getProductCount() {
        return this.productCards.count();
    }

    /**
     * Clicks on a specific product link by its index.
     * 
     * @param index 0-based index of the product link
     */
    public void clickProductLinkByIndex(int index) {
        if (index < 0 || index >= getProductCount()) {
            throw new IndexOutOfBoundsException("Product index " + index + " is out of bounds. Total products: " + getProductCount());
        }
        this.productLinks.nth(index).click();
    }

    /**
     * Retrieves the title/text of a specific product by its index.
     * 
     * @param index 0-based index of the product
     * @return the text content of the product link
     */
    public String getProductTitleByIndex(int index) {
        if (index < 0 || index >= getProductCount()) {
            throw new IndexOutOfBoundsException("Product index " + index + " is out of bounds.");
        }
        return this.productLinks.nth(index).innerText().trim();
    }

    /**
     * Checks if the product image at the specified index is visible.
     * 
     * @param index 0-based index of the product image
     * @return true if visible, false otherwise
     */
    public boolean isProductImageVisibleByIndex(int index) {
        if (index < 0 || index >= getProductCount()) {
            return false;
        }
        return this.productImages.nth(index).isVisible();
    }
}