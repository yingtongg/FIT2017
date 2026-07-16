Cypress.Commands.add('assertBlockedWith', (text) => {
  cy.get('[data-testid="readiness-badge"]').should('contain.text', 'Blocked');
  cy.get('[data-testid="readiness-reason"]')
    .should('be.visible')
    .and('contain.text', text);
  cy.get('[data-testid="btn-enrol"]').should('be.disabled');
});

Cypress.Commands.add('assertReady', () => {
  cy.get('[data-testid="readiness-badge"]').should('contain.text', 'Ready');
  // element exists but should be hidden in Ready state
  cy.get('[data-testid="readiness-reason"]').should('not.be.visible');
  cy.get('[data-testid="btn-enrol"]').should('be.enabled');
});
