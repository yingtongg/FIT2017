// cypress.config.js
module.exports = {
  e2e: {
    baseUrl: 'http://127.0.0.1:5000',
    specPattern: 'cypress/e2e/*.cy.js',      // explicit, no subfolders
    supportFile: 'cypress/support/e2e.js',    // explicit support path
    video: false,
    screenshotOnRunFailure: true
  }
};
