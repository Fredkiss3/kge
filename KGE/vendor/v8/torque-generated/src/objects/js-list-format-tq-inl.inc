template<class D, class P>
String TorqueGeneratedJSListFormat<D, P>::locale() const {
  PtrComprCageBase cage_base = GetPtrComprCageBase(*this);
  return TorqueGeneratedJSListFormat::locale(cage_base);
}

template<class D, class P>
String TorqueGeneratedJSListFormat<D, P>::locale(PtrComprCageBase cage_base) const {
  String value;
  value = TaggedField<String>::load(cage_base, *this, kLocaleOffset);
  DCHECK(value.IsString());
  return value;
}

template<class D, class P>
void TorqueGeneratedJSListFormat<D, P>::set_locale(String value, WriteBarrierMode mode) {
  SLOW_DCHECK(value.IsString());
  WRITE_FIELD(*this, kLocaleOffset, value);
  CONDITIONAL_WRITE_BARRIER(*this, kLocaleOffset, value, mode);
}

template<class D, class P>
Foreign TorqueGeneratedJSListFormat<D, P>::icu_formatter() const {
  PtrComprCageBase cage_base = GetPtrComprCageBase(*this);
  return TorqueGeneratedJSListFormat::icu_formatter(cage_base);
}

template<class D, class P>
Foreign TorqueGeneratedJSListFormat<D, P>::icu_formatter(PtrComprCageBase cage_base) const {
  Foreign value;
  value = TaggedField<Foreign>::load(cage_base, *this, kIcuFormatterOffset);
  DCHECK(value.IsForeign());
  return value;
}

template<class D, class P>
void TorqueGeneratedJSListFormat<D, P>::set_icu_formatter(Foreign value, WriteBarrierMode mode) {
  SLOW_DCHECK(value.IsForeign());
  WRITE_FIELD(*this, kIcuFormatterOffset, value);
  CONDITIONAL_WRITE_BARRIER(*this, kIcuFormatterOffset, value, mode);
}

template<class D, class P>
int TorqueGeneratedJSListFormat<D, P>::flags() const {
  int value;
  value = TaggedField<Smi>::load(*this, kFlagsOffset).value();
  return value;
}

template<class D, class P>
void TorqueGeneratedJSListFormat<D, P>::set_flags(int value) {
  WRITE_FIELD(*this, kFlagsOffset, Smi::FromInt(value));
}

template<class D, class P>
inline TorqueGeneratedJSListFormat<D, P>::TorqueGeneratedJSListFormat(Address ptr)
  : P(ptr) {
  SLOW_DCHECK(IsJSListFormat_NonInline(*this));
}
template<class D, class P>
inline TorqueGeneratedJSListFormat<D, P>::TorqueGeneratedJSListFormat(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi)
  : P(ptr, allow_smi) {
  SLOW_DCHECK((allow_smi == HeapObject::AllowInlineSmiStorage::kAllowBeingASmi && this->IsSmi()) || IsJSListFormat_NonInline(*this));
}
