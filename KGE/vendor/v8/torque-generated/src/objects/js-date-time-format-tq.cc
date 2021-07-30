#include "src/objects/js-date-time-format-inl.h"

#include "torque-generated/class-verifiers.h"
#include "src/objects/instance-type-inl.h"

namespace v8 {
namespace internal {
bool IsJSDateTimeFormat_NonInline(HeapObject o) {
  return o.IsJSDateTimeFormat();}

#ifdef VERIFY_HEAP

template <>
void TorqueGeneratedJSDateTimeFormat<JSDateTimeFormat, JSObject>::JSDateTimeFormatVerify(Isolate* isolate) {
  TorqueGeneratedClassVerifiers::JSDateTimeFormatVerify(JSDateTimeFormat::cast(*this), isolate);
}
#endif  // VERIFY_HEAP
} // namespace internal
} // namespace v8
