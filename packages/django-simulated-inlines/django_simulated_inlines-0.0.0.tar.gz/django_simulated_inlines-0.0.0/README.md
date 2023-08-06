# Django Simulated Inlines
[![Built with Spacemacs](https://cdn.rawgit.com/syl20bnr/spacemacs/442d025779da2f62fc86c2082703697714db6514/assets/spacemacs-badge.svg)](http://spacemacs.org)

## Description
This package extends the ModelAdmin interface with the possibility to create custom inlines
that can contain a list of any Model instances, the relationship with the base change_form is not needed.

## Features
  *  inlines can be collapsed
  *  supports inline subtitles
  *  pagination
  *  custom links for any inline cell
  *  dynamic fields
  *  action buttons

## Installation

1. Install: `pip install django_simulated_inlines`
2. add to INSTALLED_APPS:
```
    INSTALLED_APPS = [
        ...
        'django_simulated_inlines',
    ]
```

## How to Use
  * Import the ModelAdmin and Inline classes 
  
  ` from django_simulated_inlines.admin import SimulatedInline, SimulatedInlinesModelAdmin`

  * Declarating inlines:
  ```
  class ExampleInline(SimulatedInline):
      model = ExampleModel
      verbose_name = _("example")
      verbose_name_plural = _("examples")
      per_page = 20
      buttons = ("example_button", )
      collapse = True
      fields = (
          "id"
          ("custom_link", "/admin/custom/link/%s/"),
          "custom_field",
      )
      
      def custom_field(self, obj):
          """The return of this function is the value on the field cell"""
          return f"Custom field for {self.field}"
      custom_field.short_description = _("custom field")
      
      def example_button(self, request, object_id):
          """This function is called when the button is pressed"""
          execute_code()
      example_button.short_description = _("Execute example button")
      
      def get_subtitle(self, request, object_id):
          """Override this to define a subtitle for the inline"""
          return "this is a subtitle"
          
      def get_queryset(self, request, object_id, parent_queryset):
         """Override this to filter or customize de queryset"""
         return self.model.objects.filter(x=object_id).all()
  ```
  
  * Add the inlines to the  `SimulatedInlinesModelAdmin.simulated_inlines`.
  ```
  class ExampleModelAdmin(SimulatedInlinesModelAdmin):
      simulated_inlines = [ExampleSimulatedInline]
  ```
  
## Requirements
