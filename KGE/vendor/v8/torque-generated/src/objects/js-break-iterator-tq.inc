class JSV8BreakIterator;
// Alias for HeapObject::IsJSV8BreakIterator() that avoids inlining.
V8_EXPORT_PRIVATE bool IsJSV8BreakIterator_NonInline(HeapObject o);
template <class D, class P>
class TorqueGeneratedJSV8BreakIterator : public P {
  static_assert(std::is_same<JSV8BreakIterator, D>::value,
    "Use this class as direct base for JSV8BreakIterator.");
  static_assert(std::is_same<JSObject, P>::value,
    "Pass in JSObject as second template parameter for TorqueGeneratedJSV8BreakIterator.");
 public: 
  using Super = P;
  using TorqueGeneratedClass = TorqueGeneratedJSV8BreakIterator<D,P>;

inline String locale() const;
inline String locale(PtrComprCageBase cage_base) const;
inline void set_locale(String value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline Foreign break_iterator() const;
inline Foreign break_iterator(PtrComprCageBase cage_base) const;
inline void set_break_iterator(Foreign value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

inline Foreign unicode_string() const;
inline Foreign unicode_string(PtrComprCageBase cage_base) const;
inline void set_unicode_string(Foreign value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: (Undefined | class JSFunction)
inline HeapObject bound_adopt_text() const;
inline HeapObject bound_adopt_text(PtrComprCageBase cage_base) const;
inline void set_bound_adopt_text(HeapObject value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: (Undefined | class JSFunction)
inline HeapObject bound_first() const;
inline HeapObject bound_first(PtrComprCageBase cage_base) const;
inline void set_bound_first(HeapObject value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: (Undefined | class JSFunction)
inline HeapObject bound_next() const;
inline HeapObject bound_next(PtrComprCageBase cage_base) const;
inline void set_bound_next(HeapObject value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: (Undefined | class JSFunction)
inline HeapObject bound_current() const;
inline HeapObject bound_current(PtrComprCageBase cage_base) const;
inline void set_bound_current(HeapObject value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

  // Torque type: (Undefined | class JSFunction)
inline HeapObject bound_break_type() const;
inline HeapObject bound_break_type(PtrComprCageBase cage_base) const;
inline void set_bound_break_type(HeapObject value, WriteBarrierMode mode = UPDATE_WRITE_BARRIER);

V8_INLINE static D cast(Object object) {
  return D(object.ptr());
}

V8_INLINE static D unchecked_cast(Object object) {
  return bit_cast<D>(object);
}

#ifdef VERIFY_HEAP
V8_EXPORT_PRIVATE void JSV8BreakIteratorVerify(Isolate* isolate);
#endif  // VERIFY_HEAP

  static constexpr int kStartOfStrongFieldsOffset = P::kHeaderSize;
  static constexpr int kLocaleOffset = P::kHeaderSize;
  static constexpr int kLocaleOffsetEnd = kLocaleOffset + kTaggedSize - 1;
  static constexpr int kBreakIteratorOffset = kLocaleOffsetEnd + 1;
  static constexpr int kBreakIteratorOffsetEnd = kBreakIteratorOffset + kTaggedSize - 1;
  static constexpr int kUnicodeStringOffset = kBreakIteratorOffsetEnd + 1;
  static constexpr int kUnicodeStringOffsetEnd = kUnicodeStringOffset + kTaggedSize - 1;
  static constexpr int kBoundAdoptTextOffset = kUnicodeStringOffsetEnd + 1;
  static constexpr int kBoundAdoptTextOffsetEnd = kBoundAdoptTextOffset + kTaggedSize - 1;
  static constexpr int kBoundFirstOffset = kBoundAdoptTextOffsetEnd + 1;
  static constexpr int kBoundFirstOffsetEnd = kBoundFirstOffset + kTaggedSize - 1;
  static constexpr int kBoundNextOffset = kBoundFirstOffsetEnd + 1;
  static constexpr int kBoundNextOffsetEnd = kBoundNextOffset + kTaggedSize - 1;
  static constexpr int kBoundCurrentOffset = kBoundNextOffsetEnd + 1;
  static constexpr int kBoundCurrentOffsetEnd = kBoundCurrentOffset + kTaggedSize - 1;
  static constexpr int kBoundBreakTypeOffset = kBoundCurrentOffsetEnd + 1;
  static constexpr int kBoundBreakTypeOffsetEnd = kBoundBreakTypeOffset + kTaggedSize - 1;
  static constexpr int kEndOfStrongFieldsOffset = kBoundBreakTypeOffsetEnd + 1;
  static constexpr int kStartOfWeakFieldsOffset = kBoundBreakTypeOffsetEnd + 1;
  static constexpr int kEndOfWeakFieldsOffset = kBoundBreakTypeOffsetEnd + 1;
  static constexpr int kHeaderSize = kBoundBreakTypeOffsetEnd + 1;

  friend class Factory;

 public:
  template <class DAlias = D>
  constexpr TorqueGeneratedJSV8BreakIterator() : P() {
    static_assert(std::is_base_of<TorqueGeneratedJSV8BreakIterator, 
      DAlias>::value,
      "class TorqueGeneratedJSV8BreakIterator should be used as direct base for JSV8BreakIterator.");
  }
 protected:
  inline explicit TorqueGeneratedJSV8BreakIterator(Address ptr);
  // Special-purpose constructor for subclasses that have fast paths where
  // their ptr() is a Smi.
  inline explicit TorqueGeneratedJSV8BreakIterator(Address ptr, HeapObject::AllowInlineSmiStorage allow_smi);
};

