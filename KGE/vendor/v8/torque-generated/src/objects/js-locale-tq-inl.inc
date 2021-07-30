template<class D, class P>
Foreign TorqueGeneratedJSLocale<D, P>::icu_locale() const {
  PtrComprCageBase cage_base = GetPtrComprCageBase(*this);
  return TorqueGeneratedJSLocale::icu_locale(cage_base);
}

template<class D, class P>
Foreign TorqueGeneratedJSLocale<D, P>::icu_locale(PtrComprCageBase cage_base) const {
  Foreign value;
  value = TaggedField<Foreign>::load(cage_base, *this, kIcuLocaleOffset);
  DCHECK(value.IsForeign());
  return value;
}

template<class D, class P>
void TorqueGeneratedJSLocale<D, P>::set_icu_locale(Foreign value, WriteBarrierMode mode) {
  SLOW_DCHECK(value.IsForeign());
  WRITE_FIELD(*this, kIcuLocaleOffset, value);
  CONDITIONAL_WRITE_BARRIER(*this, kIcuLocaleOffset, value, mode);
}

template<class D, class P>
inline TorqueGeneratedJSLocale<D, P>::TorqueGeneratedJSLocale(Address ptr)
  : P(ptr) {
  SLOW_DCHECK(IsJSLocale_NonInline(*this));
}
template<class D, class P>
inline TorqueGeneratedJSLocale<D, P>::TorqueGeneratedJSLocale(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi)
  : P(ptr, allow_smi) {
  SLOW_DCHECK((allow_smi == HeapObject::AllowInlineSmiStorage::kAllowBeingASmi && this->IsSmi()) || IsJSLocale_NonInline(*this));
}
