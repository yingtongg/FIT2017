describe("Domestic OK", () => {
  it("Ready; intl rules ignored", () => {
    cy.visit("/?seed=domestic_ok");
    cy.assertReady();
  });
});
