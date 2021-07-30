#include "src/objects/js-plural-rules-inl.h"

#include "torque-generated/class-verifiers.h"
#include "src/objects/instance-type-inl.h"

namespace v8 {
namespace internal {
bool IsJSPluralRules_NonInline(HeapObject o) {
  return o.IsJSPluralRules();}

#ifdef VERIFY_HEAP

template <>
void TorqueGeneratedJSPluralRules<JSPluralRules, JSObject>::JSPluralRulesVerify(Isolate* isolate) {
  TorqueGeneratedClassVerifiers::JSPluralRulesVerify(JSPluralRules::cast(*this), isolate);
}
#endif  // VERIFY_HEAP
} // namespace internal
} // namespace v8
