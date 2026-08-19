package com.pages.playwright;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;

public class HomePage {

    private final Page page;
    private final Locator searchBox;
    private final Locator searchSubmit;

    public HomePage(Page page) {
        this.page = page;
        this.searchBox = page.locator("input#twotabsearchtextbox");
        this.searchSubmit = page.locator("input#nav-search-submit-button");
    }

    /**
     * Enters a search query into the search input field.
     * 
     * @param query The text to search for.
     */
    public void enterSearchQuery(String query) {
        this.searchBox.fill(query);
    }

    /**
     * Clicks the search submit button.
     */
    public void clickSearchButton() {
        this.searchSubmit.click();
    }

    /**
     * Performs a complete search action by typing the query and submitting.
     * 
     * @param query The text to search for.
     */
    public void performSearch(String query) {
        enterSearchQuery(query);
        clickSearchButton();
    }
}