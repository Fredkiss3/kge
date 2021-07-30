#include "src/objects/js-segmenter-inl.h"

#include "torque-generated/class-verifiers.h"
#include "src/objects/instance-type-inl.h"

namespace v8 {
namespace internal {
bool IsJSSegmenter_NonInline(HeapObject o) {
  return o.IsJSSegmenter();}

#ifdef VERIFY_HEAP

template <>
void TorqueGeneratedJSSegmenter<JSSegmenter, JSObject>::JSSegmenterVerify(Isolate* isolate) {
  TorqueGeneratedClassVerifiers::JSSegmenterVerify(JSSegmenter::cast(*this), isolate);
}
#endif  // VERIFY_HEAP
} // namespace internal
} // namespace v8
