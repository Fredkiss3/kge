#include "src/objects/module-inl.h"

#include "torque-generated/class-verifiers.h"
#include "src/objects/instance-type-inl.h"

namespace v8 {
namespace internal {
bool IsModule_NonInline(HeapObject o) {
  return o.IsModule();}

#ifdef VERIFY_HEAP

template <>
void TorqueGeneratedModule<Module, HeapObject>::ModuleVerify(Isolate* isolate) {
  TorqueGeneratedClassVerifiers::ModuleVerify(Module::cast(*this), isolate);
}
#endif  // VERIFY_HEAP
bool IsJSModuleNamespace_NonInline(HeapObject o) {
  return o.IsJSModuleNamespace();}

#ifdef VERIFY_HEAP

template <>
void TorqueGeneratedJSModuleNamespace<JSModuleNamespace, JSSpecialObject>::JSModuleNamespaceVerify(Isolate* isolate) {
  TorqueGeneratedClassVerifiers::JSModuleNamespaceVerify(JSModuleNamespace::cast(*this), isolate);
}
#endif  // VERIFY_HEAP
} // namespace internal
} // namespace v8
