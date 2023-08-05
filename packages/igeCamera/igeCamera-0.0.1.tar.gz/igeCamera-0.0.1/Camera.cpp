#include "Camera.h"
#include "CameraImpl.h"

Camera* Camera::instance = nullptr;

Camera::Camera()
	: m_cameraImpl(new CameraImpl())
{	
}
Camera::~Camera()
{	
}

void Camera::init()
{
	m_cameraImpl->Init();
}

void Camera::release()
{
	m_cameraImpl->Release();
}

uint32_t Camera::getCameraWidth()
{
	return m_cameraImpl->GetCameraWidth();
}

uint32_t Camera::getCameraHeight()
{
	return m_cameraImpl->GetCameraHeight();
}

uint8_t* Camera::getCameraData()
{
	return m_cameraImpl->GetCameraData();
}