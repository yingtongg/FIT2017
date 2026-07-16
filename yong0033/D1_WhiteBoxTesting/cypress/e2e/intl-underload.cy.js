describe("International under 12 credits", () => {
  it("Blocked with exact reason; Fix -> Ready + banner", () => {
    cy.visit("/?seed=intl_underload");
    cy.assertBlockedWith("International: current load 9 < 12");
    cy.get('[data-testid="btn-fix"]').click();
    cy.get('[data-testid="banner-success"]').should("contain.text", "Ready");
    cy.assertReady();
  });
});
