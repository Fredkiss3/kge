#include "src/objects/js-locale-inl.h"

#include "torque-generated/class-verifiers.h"
#include "src/objects/instance-type-inl.h"

namespace v8 {
namespace internal {
bool IsJSLocale_NonInline(HeapObject o) {
  return o.IsJSLocale();}

#ifdef VERIFY_HEAP

template <>
void TorqueGeneratedJSLocale<JSLocale, JSObject>::JSLocaleVerify(Isolate* isolate) {
  TorqueGeneratedClassVerifiers::JSLocaleVerify(JSLocale::cast(*this), isolate);
}
#endif  // VERIFY_HEAP
} // namespace internal
} // namespace v8
