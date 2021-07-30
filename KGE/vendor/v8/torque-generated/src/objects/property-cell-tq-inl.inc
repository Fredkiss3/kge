template<class D, class P>
Name TorqueGeneratedPropertyCell<D, P>::name() const {
  PtrComprCageBase cage_base = GetPtrComprCageBase(*this);
  return TorqueGeneratedPropertyCell::name(cage_base);
}

template<class D, class P>
Name TorqueGeneratedPropertyCell<D, P>::name(PtrComprCageBase cage_base) const {
  Name value;
  value = TaggedField<Name>::load(cage_base, *this, kNameOffset);
  DCHECK(value.IsString() || value.IsPublicSymbol() || value.IsPrivateSymbol());
  return value;
}

template<class D, class P>
void TorqueGeneratedPropertyCell<D, P>::set_name(Name value, WriteBarrierMode mode) {
  SLOW_DCHECK(value.IsString() || value.IsPublicSymbol() || value.IsPrivateSymbol());
  WRITE_FIELD(*this, kNameOffset, value);
  CONDITIONAL_WRITE_BARRIER(*this, kNameOffset, value, mode);
}

template<class D, class P>
int TorqueGeneratedPropertyCell<D, P>::property_details_raw() const {
  int value;
  value = TaggedField<Smi>::load(*this, kPropertyDetailsRawOffset).value();
  return value;
}

template<class D, class P>
void TorqueGeneratedPropertyCell<D, P>::set_property_details_raw(int value) {
  WRITE_FIELD(*this, kPropertyDetailsRawOffset, Smi::FromInt(value));
}

template<class D, class P>
Object TorqueGeneratedPropertyCell<D, P>::value() const {
  PtrComprCageBase cage_base = GetPtrComprCageBase(*this);
  return TorqueGeneratedPropertyCell::value(cage_base);
}

template<class D, class P>
Object TorqueGeneratedPropertyCell<D, P>::value(PtrComprCageBase cage_base) const {
  Object value;
  value = TaggedField<Object>::load(cage_base, *this, kValueOffset);
  DCHECK(value.IsHeapObject() || value.IsSmi());
  return value;
}

template<class D, class P>
void TorqueGeneratedPropertyCell<D, P>::set_value(Object value, WriteBarrierMode mode) {
  SLOW_DCHECK(value.IsHeapObject() || value.IsSmi());
  WRITE_FIELD(*this, kValueOffset, value);
  CONDITIONAL_WRITE_BARRIER(*this, kValueOffset, value, mode);
}

template<class D, class P>
WeakFixedArray TorqueGeneratedPropertyCell<D, P>::dependent_code() const {
  PtrComprCageBase cage_base = GetPtrComprCageBase(*this);
  return TorqueGeneratedPropertyCell::dependent_code(cage_base);
}

template<class D, class P>
WeakFixedArray TorqueGeneratedPropertyCell<D, P>::dependent_code(PtrComprCageBase cage_base) const {
  WeakFixedArray value;
  value = TaggedField<WeakFixedArray>::load(cage_base, *this, kDependentCodeOffset);
  DCHECK(value.IsDependentCode());
  return value;
}

template<class D, class P>
void TorqueGeneratedPropertyCell<D, P>::set_dependent_code(WeakFixedArray value, WriteBarrierMode mode) {
  SLOW_DCHECK(value.IsDependentCode());
  WRITE_FIELD(*this, kDependentCodeOffset, value);
  CONDITIONAL_WRITE_BARRIER(*this, kDependentCodeOffset, value, mode);
}

template<class D, class P>
inline TorqueGeneratedPropertyCell<D, P>::TorqueGeneratedPropertyCell(Address ptr)
  : P(ptr) {
  SLOW_DCHECK(IsPropertyCell_NonInline(*this));
}
template<class D, class P>
inline TorqueGeneratedPropertyCell<D, P>::TorqueGeneratedPropertyCell(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi)
  : P(ptr, allow_smi) {
  SLOW_DCHECK((allow_smi == HeapObject::AllowInlineSmiStorage::kAllowBeingASmi && this->IsSmi()) || IsPropertyCell_NonInline(*this));
}
