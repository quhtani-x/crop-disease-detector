import sys
import numpy as np
import cv2

# CROP DISEASE DETECTOR.
# farmers can photograph a leaf and this estimates how diseased it is. it finds
# the leaf, then looks for brown/yellow spots (disease) vs healthy green, and
# reports the % of the leaf that looks unhealthy + highlights the bad patches.
# a real "scout your field with your phone" tool.
#
# if you dont pass an image it makes a fake spotted leaf so it runs right away.


def make_fake_leaf():
    # a green leaf shape with some brown disease spots
    img = np.full((400, 400, 3), (30, 30, 30), np.uint8)
    cv2.ellipse(img, (200, 200), (150, 90), 30, 0, 360, (40, 160, 50), -1)  # green leaf
    # scatter brown diseased spots
    rng = np.random.default_rng(3)
    for _ in range(12):
        x, y = rng.integers(100, 300), rng.integers(140, 260)
        cv2.circle(img, (int(x), int(y)), int(rng.integers(8, 20)), (30, 90, 130), -1)
    return img


def analyze(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # healthy = green range
    green = cv2.inRange(hsv, np.array([35, 40, 40]), np.array([85, 255, 255]))
    # disease = brown / yellow range
    disease = cv2.inRange(hsv, np.array([5, 40, 40]), np.array([30, 255, 255]))

    leaf_area = cv2.countNonZero(green) + cv2.countNonZero(disease)
    diseased = cv2.countNonZero(disease)
    pct = (diseased / leaf_area * 100) if leaf_area else 0

    # outline the diseased patches in red
    cnts, _ = cv2.findContours(disease, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    out = img.copy()
    for c in cnts:
        if cv2.contourArea(c) > 30:
            cv2.drawContours(out, [c], -1, (0, 0, 255), 2)

    if pct < 5:
        verdict = "healthy"
    elif pct < 20:
        verdict = "mild disease"
    else:
        verdict = "heavily diseased - treat it"
    cv2.putText(out, f"{pct:.1f}% diseased - {verdict}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    return out, pct, verdict


def main():
    img = cv2.imread(sys.argv[1]) if len(sys.argv) > 1 else make_fake_leaf()
    out, pct, verdict = analyze(img)
    print(f"{pct:.1f}% of the leaf looks diseased -> {verdict}")
    cv2.imshow("crop disease detector (any key to close)", out)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
