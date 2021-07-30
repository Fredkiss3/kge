#include "src/objects/regexp-match-info-inl.h"

#include "torque-generated/class-verifiers.h"
#include "src/objects/instance-type-inl.h"

namespace v8 {
namespace internal {
bool IsRegExpMatchInfo_NonInline(HeapObject o) {
  return o.IsRegExpMatchInfo();}

#ifdef VERIFY_HEAP

template <>
void TorqueGeneratedRegExpMatchInfo<RegExpMatchInfo, FixedArray>::RegExpMatchInfoVerify(Isolate* isolate) {
  TorqueGeneratedClassVerifiers::RegExpMatchInfoVerify(RegExpMatchInfo::cast(*this), isolate);
}
#endif  // VERIFY_HEAP
} // namespace internal
} // namespace v8
