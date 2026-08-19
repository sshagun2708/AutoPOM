package com.pages.playwright;

import com.microsoft.playwright.Locator;
import com.microsoft.playwright.Page;

public class LoginPage {
    private final Page page;
    private final Locator emailInput;
    private final Locator continueButton;
    private final Locator passwordInput;
    private final Locator signInButton;

    public LoginPage(Page page) {
        this.page = page;
        this.emailInput = page.locator("input#ap_email");
        this.continueButton = page.locator("input#continue");
        this.passwordInput = page.locator("input#ap_password");
        this.signInButton = page.locator("input#signInSubmit");
    }

    /**
     * Enters the email address into the email input field.
     * @param email The email address to enter.
     * @return This LoginPage instance for method chaining.
     */
    public LoginPage enterEmail(String email) {
        emailInput.fill(email);
        return this;
    }

    /**
     * Clicks the continue button to proceed to the password step.
     * @return This LoginPage instance for method chaining.
     */
    public LoginPage clickContinue() {
        continueButton.click();
        return this;
    }

    /**
     * Enters the password into the password input field.
     * @param password The password to enter.
     * @return This LoginPage instance for method chaining.
     */
    public LoginPage enterPassword(String password) {
        passwordInput.fill(password);
        return this;
    }

    /**
     * Clicks the sign-in button to submit the credentials.
     */
    public void clickSignIn() {
        signInButton.click();
    }

    /**
     * Performs a complete login flow for a two-step login process.
     * @param email The email address to enter.
     * @param password The password to enter.
     */
    public void login(String email, String password) {
        enterEmail(email);
        clickContinue();
        enterPassword(password);
        clickSignIn();
    }
}