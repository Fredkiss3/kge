#pragma once
#include "headers.h"

namespace KGE {
	enum class ComponentCategory;

	typedef std::bitset<100> Signature;
	typedef std::unordered_map<std::string, int> SignatureIndexMap;

	class Hasher {
	public:
		static Signature computeSignature(ComponentCategory type, Signature& sign, bool value = true);

		static  Signature computeSignature(const std::string& type, Signature& sign, bool value = true);

		static SignatureIndexMap GetSignatureCache() {
			return s_SignatureCache;
		}

		static Signature getSignature(ComponentCategory type);

		static  Signature getSignature(const std::string& type);

	private:
		static SignatureIndexMap s_SignatureCache;
		static int s_LastIndex;
	};

}