# Gleam.io Campaign Automation SOP & Angular Bypass

Gleam campaigns (`gleam.io/...`) use AngularJS and strict OAuth / Contestant validation.

## Gleam Architecture & Mechanics
1. **Contestant Details Modal:**
   - Appears when the user enters their first action if details (Full Name, Email, Custom Questions like UID, X Handle) are missing.
   - Form inputs can be updated via DOM event dispatching (`input`, `change`) AND updating `angular.element(document.body).scope().contestantState.form`.
   - Click the visible `Save` button (`button.btn-primary` or `button:has-text('Save')`) to validate.

2. **X / Social OAuth Flow:**
   - Gleam opens an X OAuth popup (`x.com/i/oauth2/authorize?...`).
   - Find the open tab in CDP, evaluate click on `[data-testid="OAuth_Consent_Button"]` or button containing `Izinkan aplikasi` / `Authorize app`.
   - The popup redirects to `gleam.io/contestant_backdoor/resume_oauth/twitter` and closes itself.

3. **Bypassing / Triggering Actions via AngularJS:**
   - Each entry method has an Angular scope holding `entry_method`.
   - To trigger and confirm:
     ```javascript
     const scope = angular.element(entryMethodEl).scope();
     if (scope && scope.entry_method) {
         // Trigger visit tracking
         scope.triggerVisit(scope.entry_method);
         // Confirm action completion
         scope.confirmAction(scope.entry_method, scope.entryState.formData[scope.entry_method.id] || {});
         scope.$apply();
     }
     ```
   - For question/UID fields: fill the `textarea`/`input` inside the entry method container, then trigger `Continue`.

4. **Proof of Claim:**
   - Gleam top bar changes: `Your Entries` increments (e.g. from `0` to `3`).
   - Completed action row changes class to `completed-entry-method` with a checkmark badge.
