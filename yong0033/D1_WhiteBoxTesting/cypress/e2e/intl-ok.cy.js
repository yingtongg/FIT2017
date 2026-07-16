describe("International OK", () => {
  it("Ready and Enrol enabled", () => {
    cy.visit("/?seed=intl_ok");
    cy.assertReady();
  });
});
