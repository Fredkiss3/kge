#include "src/objects/property-cell-inl.h"

#include "torque-generated/class-verifiers.h"
#include "src/objects/instance-type-inl.h"

namespace v8 {
namespace internal {
bool IsPropertyCell_NonInline(HeapObject o) {
  return o.IsPropertyCell();}

#ifdef VERIFY_HEAP

template <>
void TorqueGeneratedPropertyCell<PropertyCell, HeapObject>::PropertyCellVerify(Isolate* isolate) {
  TorqueGeneratedClassVerifiers::PropertyCellVerify(PropertyCell::cast(*this), isolate);
}
#endif  // VERIFY_HEAP
} // namespace internal
} // namespace v8
