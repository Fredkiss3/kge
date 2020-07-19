#include "headers.h"
#include "Hasher.h"
#include "Component.h"

namespace KGE {
	int Hasher::s_LastIndex{ 0 };
	SignatureIndexMap Hasher::s_SignatureCache;

	Signature Hasher::computeSignature(ComponentCategory type, Signature& sign, bool value) {
		sign[(int)type] = value;
		return sign;
	}

	Signature Hasher::computeSignature(const std::string& type, Signature& sign, bool value) {

		if (s_SignatureCache.find(type) != s_SignatureCache.end()) {
			sign[s_SignatureCache[type]] = value;
		}
		else
		{
			sign[s_LastIndex] = value;
			s_SignatureCache[type] = s_LastIndex;
			++s_LastIndex;
		}

		return sign;
	}

	Signature Hasher::getSignature(ComponentCategory type) {
		Signature sign;
		sign[(int)type] = true;
		return sign;
	}

	Signature Hasher::getSignature(const std::string& type) {
		Signature sign;
		if (s_SignatureCache.find(type) != s_SignatureCache.end()) {
			sign[s_SignatureCache[type]] = true;
		}
		else
		{
			sign[s_LastIndex] = true;
			s_SignatureCache[type] = s_LastIndex;
			++s_LastIndex;
		}

		return sign;
	}

}