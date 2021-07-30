#include "src/objects/js-segment-iterator-inl.h"

#include "torque-generated/class-verifiers.h"
#include "src/objects/instance-type-inl.h"

namespace v8 {
namespace internal {
bool IsJSSegmentIterator_NonInline(HeapObject o) {
  return o.IsJSSegmentIterator();}

#ifdef VERIFY_HEAP

template <>
void TorqueGeneratedJSSegmentIterator<JSSegmentIterator, JSObject>::JSSegmentIteratorVerify(Isolate* isolate) {
  TorqueGeneratedClassVerifiers::JSSegmentIteratorVerify(JSSegmentIterator::cast(*this), isolate);
}
#endif  // VERIFY_HEAP
} // namespace internal
} // namespace v8
