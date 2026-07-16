describe("International online cap", () => {
  it("blocks when >2 Online; Fix converts -> Ready", () => {
    cy.visit("/?seed=intl_online_limit");
    cy.assertBlockedWith("International: online unit limit exceeded");
    cy.get('[data-testid="btn-fix"]').click();
    cy.get('[data-testid="banner-success"]').should("contain.text", "Ready");
    cy.assertReady();
  });
});
