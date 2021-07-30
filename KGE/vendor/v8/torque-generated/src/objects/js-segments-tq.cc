#include "src/objects/js-segments-inl.h"

#include "torque-generated/class-verifiers.h"
#include "src/objects/instance-type-inl.h"

namespace v8 {
namespace internal {
bool IsJSSegments_NonInline(HeapObject o) {
  return o.IsJSSegments();}

#ifdef VERIFY_HEAP

template <>
void TorqueGeneratedJSSegments<JSSegments, JSObject>::JSSegmentsVerify(Isolate* isolate) {
  TorqueGeneratedClassVerifiers::JSSegmentsVerify(JSSegments::cast(*this), isolate);
}
#endif  // VERIFY_HEAP
} // namespace internal
} // namespace v8
