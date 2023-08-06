## 3.0.1

Changed login behaviour: replace history entry (of the login form) rather than creating a new one.
This is really how it should have worked all along.

# 3.0.0

Breaking changes:

Renamed the following data-* attributes to qnc-* (from utils.js):
    - qnc-link
    - qnc-replace-location
    - qnc-confirm-first
    - qnc-add-row-to-formset
    - qnc-formset-template
    - qnc-formset-container
    - qnc-ajax-submit-on-change

In your templates, you should be able to replace: 
    data-(link|replace-location|ajax-submit-on-change|formset-container|formset-template|add-row-to-formset|confirm-first)
With:
    qnc-$1

## 2.1.1

Added TrueFalseField

## 2.1.0

Changed login behaviour

## 2.0.1

Added missing files to build

# 2.0.0

Implemented custom log in/out views

## 1.0.2

Added templates and static files to package

# 1.0.0

Breaking changes:
- Renamed forms.css -> qnc_crud.css
- Changed css classes used by complete_form.html
- SmartBackButton only appears if history.back() will succeed

Added:
- form test page
- all_scripts_and_styles.html
- SmartBackButton added can_go_back() and can_go_back_to_same_domain() utilities
- reload_restoration.js

## 0.1.0

Added permissions helpers, using django_early_return

# 0.0.0