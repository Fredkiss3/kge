template<class D, class P>
ObjectHashTable TorqueGeneratedModule<D, P>::exports() const {
  PtrComprCageBase cage_base = GetPtrComprCageBase(*this);
  return TorqueGeneratedModule::exports(cage_base);
}

template<class D, class P>
ObjectHashTable TorqueGeneratedModule<D, P>::exports(PtrComprCageBase cage_base) const {
  ObjectHashTable value;
  value = TaggedField<ObjectHashTable>::load(cage_base, *this, kExportsOffset);
  DCHECK(value.IsObjectHashTable());
  return value;
}

template<class D, class P>
void TorqueGeneratedModule<D, P>::set_exports(ObjectHashTable value, WriteBarrierMode mode) {
  SLOW_DCHECK(value.IsObjectHashTable());
  WRITE_FIELD(*this, kExportsOffset, value);
  CONDITIONAL_WRITE_BARRIER(*this, kExportsOffset, value, mode);
}

template<class D, class P>
int TorqueGeneratedModule<D, P>::hash() const {
  int value;
  value = TaggedField<Smi>::load(*this, kHashOffset).value();
  return value;
}

template<class D, class P>
void TorqueGeneratedModule<D, P>::set_hash(int value) {
  WRITE_FIELD(*this, kHashOffset, Smi::FromInt(value));
}

template<class D, class P>
int TorqueGeneratedModule<D, P>::status() const {
  int value;
  value = TaggedField<Smi>::load(*this, kStatusOffset).value();
  return value;
}

template<class D, class P>
void TorqueGeneratedModule<D, P>::set_status(int value) {
  WRITE_FIELD(*this, kStatusOffset, Smi::FromInt(value));
}

template<class D, class P>
HeapObject TorqueGeneratedModule<D, P>::module_namespace() const {
  PtrComprCageBase cage_base = GetPtrComprCageBase(*this);
  return TorqueGeneratedModule::module_namespace(cage_base);
}

template<class D, class P>
HeapObject TorqueGeneratedModule<D, P>::module_namespace(PtrComprCageBase cage_base) const {
  HeapObject value;
  value = TaggedField<HeapObject>::load(cage_base, *this, kModuleNamespaceOffset);
  DCHECK(value.IsUndefined() || value.IsJSModuleNamespace());
  return value;
}

template<class D, class P>
void TorqueGeneratedModule<D, P>::set_module_namespace(HeapObject value, WriteBarrierMode mode) {
  SLOW_DCHECK(value.IsUndefined() || value.IsJSModuleNamespace());
  WRITE_FIELD(*this, kModuleNamespaceOffset, value);
  CONDITIONAL_WRITE_BARRIER(*this, kModuleNamespaceOffset, value, mode);
}

template<class D, class P>
Object TorqueGeneratedModule<D, P>::exception() const {
  PtrComprCageBase cage_base = GetPtrComprCageBase(*this);
  return TorqueGeneratedModule::exception(cage_base);
}

template<class D, class P>
Object TorqueGeneratedModule<D, P>::exception(PtrComprCageBase cage_base) const {
  Object value;
  value = TaggedField<Object>::load(cage_base, *this, kExceptionOffset);
  DCHECK(value.IsHeapObject() || value.IsSmi());
  return value;
}

template<class D, class P>
void TorqueGeneratedModule<D, P>::set_exception(Object value, WriteBarrierMode mode) {
  SLOW_DCHECK(value.IsHeapObject() || value.IsSmi());
  WRITE_FIELD(*this, kExceptionOffset, value);
  CONDITIONAL_WRITE_BARRIER(*this, kExceptionOffset, value, mode);
}

template<class D, class P>
HeapObject TorqueGeneratedModule<D, P>::top_level_capability() const {
  PtrComprCageBase cage_base = GetPtrComprCageBase(*this);
  return TorqueGeneratedModule::top_level_capability(cage_base);
}

template<class D, class P>
HeapObject TorqueGeneratedModule<D, P>::top_level_capability(PtrComprCageBase cage_base) const {
  HeapObject value;
  value = TaggedField<HeapObject>::load(cage_base, *this, kTopLevelCapabilityOffset);
  DCHECK(value.IsUndefined() || value.IsJSPromise());
  return value;
}

template<class D, class P>
void TorqueGeneratedModule<D, P>::set_top_level_capability(HeapObject value, WriteBarrierMode mode) {
  SLOW_DCHECK(value.IsUndefined() || value.IsJSPromise());
  WRITE_FIELD(*this, kTopLevelCapabilityOffset, value);
  CONDITIONAL_WRITE_BARRIER(*this, kTopLevelCapabilityOffset, value, mode);
}

template<class D, class P>
inline TorqueGeneratedModule<D, P>::TorqueGeneratedModule(Address ptr)
  : P(ptr) {
  SLOW_DCHECK(IsModule_NonInline(*this));
}
template<class D, class P>
inline TorqueGeneratedModule<D, P>::TorqueGeneratedModule(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi)
  : P(ptr, allow_smi) {
  SLOW_DCHECK((allow_smi == HeapObject::AllowInlineSmiStorage::kAllowBeingASmi && this->IsSmi()) || IsModule_NonInline(*this));
}
template<class D, class P>
Module TorqueGeneratedJSModuleNamespace<D, P>::module() const {
  PtrComprCageBase cage_base = GetPtrComprCageBase(*this);
  return TorqueGeneratedJSModuleNamespace::module(cage_base);
}

template<class D, class P>
Module TorqueGeneratedJSModuleNamespace<D, P>::module(PtrComprCageBase cage_base) const {
  Module value;
  value = TaggedField<Module>::load(cage_base, *this, kModuleOffset);
  DCHECK(value.IsModule());
  return value;
}

template<class D, class P>
void TorqueGeneratedJSModuleNamespace<D, P>::set_module(Module value, WriteBarrierMode mode) {
  SLOW_DCHECK(value.IsModule());
  WRITE_FIELD(*this, kModuleOffset, value);
  CONDITIONAL_WRITE_BARRIER(*this, kModuleOffset, value, mode);
}

template<class D, class P>
inline TorqueGeneratedJSModuleNamespace<D, P>::TorqueGeneratedJSModuleNamespace(Address ptr)
  : P(ptr) {
  SLOW_DCHECK(IsJSModuleNamespace_NonInline(*this));
}
template<class D, class P>
inline TorqueGeneratedJSModuleNamespace<D, P>::TorqueGeneratedJSModuleNamespace(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi)
  : P(ptr, allow_smi) {
  SLOW_DCHECK((allow_smi == HeapObject::AllowInlineSmiStorage::kAllowBeingASmi && this->IsSmi()) || IsJSModuleNamespace_NonInline(*this));
}
