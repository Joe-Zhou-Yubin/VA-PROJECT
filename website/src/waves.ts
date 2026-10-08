export interface Ripple { x: number; z: number; born: number; strength: number }
export const MAX_RIPPLES = 18;
export const RIPPLE_LIFETIME = 3.8;
export const clamp = (n: number, lo: number, hi: number) => Math.max(lo, Math.min(hi, n));

// x is lateral world pixels, z is 0 at the horizon and 1000 in the foreground.
// Height is in world pixels, positive upward. All actors sample this same field.
export function sampleWater(x: number, z: number, time: number, ripples: readonly Ripple[]) {
  let height = 35 * Math.sin(x * .006 + z * .012 - time * .52)
    + 19 * Math.sin(x * .010 - z * .018 + time * .37)
    + 9 * Math.sin(x * .017 + z * .027 - time * .69);
  for (const ripple of ripples) {
    const age = time - ripple.born;
    if (age < 0 || age > RIPPLE_LIFETIME) continue;
    const distance = Math.hypot(x - ripple.x, (z - ripple.z) * 1.25);
    const ring = distance - age * 170;
    height += ripple.strength * Math.exp(-age * .88) * Math.exp(-(ring * ring) / 14000) * Math.sin(ring * .043);
  }
  return height;
}

export function expireRipples(ripples: Ripple[], time: number) {
  while (ripples.length && time - ripples[0].born > RIPPLE_LIFETIME) ripples.shift();
}

export function addRipple(ripples: Ripple[], ripple: Ripple) {
  ripples.push(ripple);
  if (ripples.length > MAX_RIPPLES) ripples.shift();
}

export function depthScale(depth: number) { return .16 + .84 * depth; }
export function project(x: number, z: number, height: number, width: number, horizon: number, range: number) {
  const depth = z / 1000, scale = depthScale(depth);
  return { x: width / 2 + x * scale, y: horizon + Math.pow(depth, 1.65) * range - height * scale, scale };
}
export function unprojectBase(sx: number, sy: number, width: number, horizon: number, range: number) {
  const depth = Math.pow(clamp((sy - horizon) / range, 0, 1.2), 1 / 1.65);
  return { x: (sx - width / 2) / depthScale(depth), z: depth * 1000 };
}
