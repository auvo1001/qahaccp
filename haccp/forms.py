from django import forms
from haccp.models import QuatForm, Technician, Manager
from django.core.urlresolvers import reverse

class QuatFormTech(forms.ModelForm):
  
    class Meta:
        model = QuatForm
        exclude=['manager_name','manager_initial','is_reviewed_date','is_reviewed']
        #=======================================================================
        # fields =['techincian_name','technician_initial',
        #          'hand_pallet_sanitizer_strength',
        #          'footbath1_sanitizer_strength',
        #          'footbath2_sanitizer_strength',
        #          'footbath3_sanitizer_strength',
        #          'footbath4_sanitizer_strength',
        #          'footbath5_sanitizer_strength',
        #          'assembly_sanitizer_strength',
        #          ]
        # 
        #=======================================================================

class QuatFormMan(forms.ModelForm):
    manager_name = forms.CharField(max_length =255)
    manager_initial = forms.CharField(max_length=5) 
    class Meta:
        model = QuatForm
        exclude = ['techincian_name','technician_initial',
                 'hand_pallet_sanitizer_strength',
                 'footbath1_sanitizer_strength',
                 'footbath2_sanitizer_strength',
                 'footbath3_sanitizer_strength',
                 'footbath4_sanitizer_strength',
                 'footbath5_sanitizer_strength',
                 'assembly_sanitizer_strength',
                ]
