#include "FirebaseMLKit.h"
#include "FirebaseMLKitImpl.h"

FirebaseMLKit* FirebaseMLKit::instance = nullptr;
using namespace firebase;

FirebaseMLKit::FirebaseMLKit()
	: m_firebaseMLKitImpl(new FirebaseMLKitImpl())
{
	LOG("FirebaseMLKit()");
}
FirebaseMLKit::~FirebaseMLKit()
{
	LOG("~FirebaseMLKit()");
}

void FirebaseMLKit::init()
{
	m_firebaseMLKitImpl->Init();
}

void FirebaseMLKit::release()
{
	m_firebaseMLKitImpl->Release();
}

void FirebaseMLKit::preview()
{
	m_firebaseMLKitImpl->Preview();
}

float* FirebaseMLKit::getContours(int& size)
{
	return m_firebaseMLKitImpl->GetContours(size);
}

float FirebaseMLKit::getHeadEulerAngleY()
{
	return m_firebaseMLKitImpl->GetHeadEulerAngleY();
}

float FirebaseMLKit::getHeadEulerAngleZ()
{
	return m_firebaseMLKitImpl->GetHeadEulerAngleZ();
}