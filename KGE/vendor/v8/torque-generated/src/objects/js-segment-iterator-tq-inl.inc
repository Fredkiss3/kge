template<class D, class P>
Foreign TorqueGeneratedJSSegmentIterator<D, P>::icu_break_iterator() const {
  PtrComprCageBase cage_base = GetPtrComprCageBase(*this);
  return TorqueGeneratedJSSegmentIterator::icu_break_iterator(cage_base);
}

template<class D, class P>
Foreign TorqueGeneratedJSSegmentIterator<D, P>::icu_break_iterator(PtrComprCageBase cage_base) const {
  Foreign value;
  value = TaggedField<Foreign>::load(cage_base, *this, kIcuBreakIteratorOffset);
  DCHECK(value.IsForeign());
  return value;
}

template<class D, class P>
void TorqueGeneratedJSSegmentIterator<D, P>::set_icu_break_iterator(Foreign value, WriteBarrierMode mode) {
  SLOW_DCHECK(value.IsForeign());
  WRITE_FIELD(*this, kIcuBreakIteratorOffset, value);
  CONDITIONAL_WRITE_BARRIER(*this, kIcuBreakIteratorOffset, value, mode);
}

template<class D, class P>
Foreign TorqueGeneratedJSSegmentIterator<D, P>::unicode_string() const {
  PtrComprCageBase cage_base = GetPtrComprCageBase(*this);
  return TorqueGeneratedJSSegmentIterator::unicode_string(cage_base);
}

template<class D, class P>
Foreign TorqueGeneratedJSSegmentIterator<D, P>::unicode_string(PtrComprCageBase cage_base) const {
  Foreign value;
  value = TaggedField<Foreign>::load(cage_base, *this, kUnicodeStringOffset);
  DCHECK(value.IsForeign());
  return value;
}

template<class D, class P>
void TorqueGeneratedJSSegmentIterator<D, P>::set_unicode_string(Foreign value, WriteBarrierMode mode) {
  SLOW_DCHECK(value.IsForeign());
  WRITE_FIELD(*this, kUnicodeStringOffset, value);
  CONDITIONAL_WRITE_BARRIER(*this, kUnicodeStringOffset, value, mode);
}

template<class D, class P>
int TorqueGeneratedJSSegmentIterator<D, P>::flags() const {
  int value;
  value = TaggedField<Smi>::load(*this, kFlagsOffset).value();
  return value;
}

template<class D, class P>
void TorqueGeneratedJSSegmentIterator<D, P>::set_flags(int value) {
  WRITE_FIELD(*this, kFlagsOffset, Smi::FromInt(value));
}

template<class D, class P>
inline TorqueGeneratedJSSegmentIterator<D, P>::TorqueGeneratedJSSegmentIterator(Address ptr)
  : P(ptr) {
  SLOW_DCHECK(IsJSSegmentIterator_NonInline(*this));
}
template<class D, class P>
inline TorqueGeneratedJSSegmentIterator<D, P>::TorqueGeneratedJSSegmentIterator(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi)
  : P(ptr, allow_smi) {
  SLOW_DCHECK((allow_smi == HeapObject::AllowInlineSmiStorage::kAllowBeingASmi && this->IsSmi()) || IsJSSegmentIterator_NonInline(*this));
}
