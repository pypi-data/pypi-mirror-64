import math
import numpy as np
from math import sqrt, atan2, pi, cos, sin

def txyzRxyz_2_pose(xyzrpw):
    """Returns the pose given the position (M) and Euler angles (rad) as an array [x,y,z,rx,ry,rz].
    The result is the same as calling: H = transl(x,y,z)*rotx(rx)*roty(ry)*rotz(rz)

    :param xyzrpw: [x,y,z,rx,ry,rz] in mm and radians
    :type xyzrpw: list of floats
    """
    [x,y,z,rx,ry,rz] = xyzrpw
    srx = math.sin(rx);
    crx = math.cos(rx);
    sry = math.sin(ry);
    cry = math.cos(ry);
    srz = math.sin(rz);
    crz = math.cos(rz);
    H = np.array([[ cry*crz, -cry*srz, sry, x],
                  [crx*srz + crz*srx*sry, crx*crz - srx*sry*srz, -cry*srx, y],
                  [srx*srz - crx*crz*sry, crz*srx + crx*sry*srz, crx*cry, z],
                  [0,0,0,1]])
    return H

def UR_2_Pose(xyzwpr):
    """Calculate the pose target given a p[x,y,z,u,v,w] cartesian target with rotation vector.
        This is the same format required by Universal Robot controllers.
    """
    x,y,z,w,p,r = xyzwpr
    wpr = [w,p,r]
    angle = norm(wpr)
    cosang = cos(0.5*angle)

    if angle == 0.0:
        q234 = [0.0,0.0,0.0]
    else:
        ratio = sin(0.5*angle)/angle
        q234 = mult3(wpr, ratio)

    q1234 = [cosang, q234[0], q234[1], q234[2]]
    pose = quaternion_2_pose(q1234)
    pose[0,3] = x
    pose[1,3] = y
    pose[2,3] = z
    return pose


def Pose_2_TxyzRxyz(H):
    """Retrieve the position (M) and Euler angles (rad) as an array [x,y,z,rx,ry,rz] given a pose.
    It returns the values that correspond to the following operation:
    H = transl(x,y,z)*rotx(rx)*roty(ry)*rotz(rz).
    """
    x = H[0,3]
    y = H[1,3]
    z = H[2,3]
    a = H[0,0]
    b = H[0,1]
    c = H[0,2]
    d = H[1,2]
    e = H[2,2]
    if c > (1.0 - 1e-6):
        ry1 = pi/2
        rx1 = 0
        rz1 = atan2(H[1,0],H[1,1])
    elif c < (-1.0 + 1e-6):
        ry1 = -pi/2
        rx1 = 0
        rz1 = atan2(H[1,0],H[1,1])
    else:
        sy = c
        cy1 = +sqrt(1-sy*sy)
        sx1 = -d/cy1
        cx1 = e/cy1
        sz1 = -b/cy1
        cz1 =a/cy1
        rx1 = atan2(sx1,cx1)
        ry1 = atan2(sy,cy1)
        rz1 = atan2(sz1,cz1)
    return [x, y, z, rx1, ry1, rz1]


def quaternion_2_pose(qin):
    """Returns the pose orientation matrix (4x4 matrix) given a quaternion orientation vector
    """
    qnorm = sqrt(qin[0]*qin[0]+qin[1]*qin[1]+qin[2]*qin[2]+qin[3]*qin[3])
    q = qin
    q[0] = q[0]/qnorm
    q[1] = q[1]/qnorm
    q[2] = q[2]/qnorm
    q[3] = q[3]/qnorm
    pose = np.array([[1 - 2*q[2]*q[2] - 2*q[3]*q[3], 2*q[1]*q[2] - 2*q[3]*q[0], 2*q[1]*q[3] + 2*q[2]*q[0], 0],
          [2*q[1]*q[2] + 2*q[3]*q[0], 1 - 2*q[1]*q[1] - 2*q[3]*q[3], 2*q[2]*q[3] - 2*q[1]*q[0], 0],
          [2*q[1]*q[3] - 2*q[2]*q[0], 2*q[2]*q[3] + 2*q[1]*q[0], 1 - 2*q[1]*q[1] - 2*q[2]*q[2], 0],
          [0 , 0 , 0 , 1]])
    return pose


def mult3(v,d):
    """Multiplies a 3D vector to a scalar"""
    return [v[0]*d, v[1]*d, v[2]*d]


def norm(p):
    """Returns the norm of a 3D vector"""
    return sqrt(p[0]*p[0] + p[1]*p[1] + p[2]*p[2])


def circle_radius(p0,p1,p2):
    a = norm(subs3(p0,p1))
    b = norm(subs3(p1,p2))
    c = norm(subs3(p2,p0))
    radius = a*b*c/sqrt(pow(a*a+b*b+c*c,2)-2*(pow(a,4)+pow(b,4)+pow(c,4)))
    return radius


def subs3(a,b):
    """Subtracts two 3D vectors c=a-b"""
    return [a[0]-b[0],a[1]-b[1],a[2]-b[2]]

def rot_x(rx):
    crx = math.cos(rx)
    srx = math.sin(rx)

    return np.array([[1,0,0,0], [0,crx,-srx,0], [0,srx,crx,0], [0,0,0,1]])

def rot_y(ry):
    crx = math.cos(ry)
    srx = math.sin(ry)

    return np.array([[crx,0,-srx,0], [0,1,0,0], [srx,0,crx,0], [0,0,0,1]])

def rot_z(rz):
    crx = math.cos(rz)
    srx = math.sin(rz)

    return np.array([[crx,-srx,0,0], [srx,crx,0,0], [0,0,1,0], [0,0,0,1]])

def transl(tx,ty=None,tz=None):
    """Returns a translation matrix (M)
    :param float tx: translation along the X axis
    :param float ty: translation along the Y axis
    :param float tz: translation along the Z axis
    """
    if ty is None:
        xx = tx[0]
        yy = tx[1]
        zz = tx[2]
    else:
        xx = tx
        yy = ty
        zz = tz
    return np.array([[1,0,0,xx],[0,1,0,yy],[0,0,1,zz],[0,0,0,1]])

def offset(target_position, refference_frame):
    """Calculates a relative target with respect to the reference frame coordinates.
    X,Y,Z are in mm, RX,RY,RZ are in degrees.
    """
    x, y, z, rx, ry, rz = refference_frame
    target_pose = xyzrpw_2_pose(target_position)

    # new_target = transl(x,y,z).dot(rot_x(rx*math.pi/180.0)).dot(rot_y(ry*math.pi/180.0)).dot(rot_z(rz*math.pi/180.0)).dot(target_pose)
    new_target = transl(x,y,z).dot(rot_x(rx)).dot(rot_y(ry)).dot(rot_z(rz)).dot(target_pose)
    new_target = pose_2_xyzrpw(new_target)

    return new_target