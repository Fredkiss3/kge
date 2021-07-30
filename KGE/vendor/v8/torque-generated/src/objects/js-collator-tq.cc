#include "src/objects/js-collator-inl.h"

#include "torque-generated/class-verifiers.h"
#include "src/objects/instance-type-inl.h"

namespace v8 {
namespace internal {
bool IsJSCollator_NonInline(HeapObject o) {
  return o.IsJSCollator();}

#ifdef VERIFY_HEAP

template <>
void TorqueGeneratedJSCollator<JSCollator, JSObject>::JSCollatorVerify(Isolate* isolate) {
  TorqueGeneratedClassVerifiers::JSCollatorVerify(JSCollator::cast(*this), isolate);
}
#endif  // VERIFY_HEAP
} // namespace internal
} // namespace v8
