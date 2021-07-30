#include "src/objects/js-relative-time-format-inl.h"

#include "torque-generated/class-verifiers.h"
#include "src/objects/instance-type-inl.h"

namespace v8 {
namespace internal {
bool IsJSRelativeTimeFormat_NonInline(HeapObject o) {
  return o.IsJSRelativeTimeFormat();}

#ifdef VERIFY_HEAP

template <>
void TorqueGeneratedJSRelativeTimeFormat<JSRelativeTimeFormat, JSObject>::JSRelativeTimeFormatVerify(Isolate* isolate) {
  TorqueGeneratedClassVerifiers::JSRelativeTimeFormatVerify(JSRelativeTimeFormat::cast(*this), isolate);
}
#endif  // VERIFY_HEAP
} // namespace internal
} // namespace v8
