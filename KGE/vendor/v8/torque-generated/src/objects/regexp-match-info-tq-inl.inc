template<class D, class P>
inline TorqueGeneratedRegExpMatchInfo<D, P>::TorqueGeneratedRegExpMatchInfo(Address ptr)
  : P(ptr) {
  SLOW_DCHECK(IsRegExpMatchInfo_NonInline(*this));
}
template<class D, class P>
inline TorqueGeneratedRegExpMatchInfo<D, P>::TorqueGeneratedRegExpMatchInfo(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi)
  : P(ptr, allow_smi) {
  SLOW_DCHECK((allow_smi == HeapObject::AllowInlineSmiStorage::kAllowBeingASmi && this->IsSmi()) || IsRegExpMatchInfo_NonInline(*this));
}
