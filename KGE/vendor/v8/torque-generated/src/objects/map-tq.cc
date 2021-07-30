#include "src/objects/map-inl.h"

#include "torque-generated/class-verifiers.h"
#include "src/objects/instance-type-inl.h"

namespace v8 {
namespace internal {
bool IsMap_NonInline(HeapObject o) {
  return o.IsMap();}

#ifdef VERIFY_HEAP

template <>
void TorqueGeneratedMap<Map, HeapObject>::MapVerify(Isolate* isolate) {
  TorqueGeneratedClassVerifiers::MapVerify(Map::cast(*this), isolate);
}
#endif  // VERIFY_HEAP
} // namespace internal
} // namespace v8
