class DataHandler;
// Alias for HeapObject::IsDataHandler() that avoids inlining.
V8_EXPORT_PRIVATE bool IsDataHandler_NonInline(HeapObject o);
template <class D, class P>
class TorqueGeneratedDataHandler : public P {
  static_assert(std::is_same<DataHandler, D>::value,
    "Use this class as direct base for DataHandler.");
  static_assert(std::is_same<Struct, P>::value,
    "Pass in Struct as second template parameter for TorqueGeneratedDataHandler.");
 public: 
  using Super = P;
  using TorqueGeneratedClass = TorqueGeneratedDataHandler<D,P>;

  // Torque type: (Smi | class Code)
inline Object smi_handler() const;
inline Object smi_handler(PtrComprCageBase cage_base) const;
inline void set_smi_handler(Object value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: (Smi | class Cell)
inline Object validity_cell() const;
inline Object validity_cell(PtrComprCageBase cage_base) const;
inline void set_validity_cell(Object value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: MaybeObject
inline MaybeObject data1() const;
inline MaybeObject data1(PtrComprCageBase cage_base) const;
inline void set_data1(MaybeObject value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: MaybeObject
inline MaybeObject data2() const;
inline MaybeObject data2(PtrComprCageBase cage_base) const;
inline void set_data2(MaybeObject value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: MaybeObject
inline MaybeObject data3() const;
inline MaybeObject data3(PtrComprCageBase cage_base) const;
inline void set_data3(MaybeObject value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

V8_INLINE static D cast(Object object) {
  return D(object.ptr());
}

V8_INLINE static D unchecked_cast(Object object) {
  return bit_cast<D>(object);
}

#ifdef VERIFY_HEAP
V8_EXPORT_PRIVATE void DataHandlerVerify(Isolate* isolate);
#endif  // VERIFY_HEAP

  static constexpr int kStartOfStrongFieldsOffset = P::kHeaderSize;
  static constexpr int kSmiHandlerOffset = P::kHeaderSize;
  static constexpr int kSmiHandlerOffsetEnd = kSmiHandlerOffset + kTaggedSize - 1;
  static constexpr int kValidityCellOffset = kSmiHandlerOffsetEnd + 1;
  static constexpr int kValidityCellOffsetEnd = kValidityCellOffset + kTaggedSize - 1;
  static constexpr int kData1Offset = kValidityCellOffsetEnd + 1;
  static constexpr int kData1OffsetEnd = kData1Offset + kTaggedSize - 1;
  static constexpr int kData2Offset = kData1OffsetEnd + 1;
  static constexpr int kData2OffsetEnd = kData2Offset + kTaggedSize - 1;
  static constexpr int kData3Offset = kData2OffsetEnd + 1;
  static constexpr int kData3OffsetEnd = kData3Offset + kTaggedSize - 1;
  static constexpr int kEndOfStrongFieldsOffset = kData3OffsetEnd + 1;
  static constexpr int kStartOfWeakFieldsOffset = kData3OffsetEnd + 1;
  static constexpr int kEndOfWeakFieldsOffset = kData3OffsetEnd + 1;
  static constexpr int kHeaderSize = kData3OffsetEnd + 1;

  friend class Factory;

 public:
  template <class DAlias = D>
  constexpr TorqueGeneratedDataHandler() : P() {
    static_assert(std::is_base_of<TorqueGeneratedDataHandler, 
      DAlias>::value,
      "class TorqueGeneratedDataHandler should be used as direct base for DataHandler.");
  }
 protected:
  inline explicit TorqueGeneratedDataHandler(Address ptr);
  // Special-purpose constructor for subclasses that have fast paths where
  // their ptr() is a Smi.
  inline explicit TorqueGeneratedDataHandler(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi);
};

