// Template renderer: captures + avatar placeholder cards + burned-in captions, then lays the
// narration clips (build/audio/<name>.aiff) under it. Edit TITLE, OUTPUT and segs, then run
// `swift render-template.swift` from the film's build/ folder. Frames are read from ../captures/.
import AppKit
import AVFoundation

let W = 1920, H = 1080
let fps: Int32 = 30
let TITLE = "<Film title> · DRAFT"   // small header shown top-left on every frame
let OUTPUT = "film-draft.mp4"        // written to the film folder
let root = URL(fileURLWithPath: FileManager.default.currentDirectoryPath).deletingLastPathComponent()
let caps = root.appendingPathComponent("captures")
let audioDir = root.appendingPathComponent("build/audio")

enum Kind { case avatar, shot(String), outro(String) }
struct Seg { let kind: Kind; let caption: String; let audio: String; var note: String? = nil }

let segs: [Seg] = [
    Seg(kind: .avatar, caption: "<Opening line, said by the presenter>", audio: "line1"),
    Seg(kind: .shot("02-<shot>.jpg"), caption: "<Caption for shot 2>", audio: "line2"),
    Seg(kind: .shot("03-<shot>.jpg"), caption: "<Caption for shot 3>", audio: "line3", note: "STAND-IN — replace with the real step"),
    Seg(kind: .outro("03-<shot>.jpg"), caption: "<Closing line>", audio: "line4"),
]

func audioURL(_ name: String) -> URL { audioDir.appendingPathComponent("\(name).aiff") }
func seconds(_ url: URL) -> Double { AVURLAsset(url: url).duration.seconds }

// Each segment lasts its narration plus a short beat; the last one holds a little longer.
let durations: [Double] = segs.enumerated().map { i, s in
    seconds(audioURL(s.audio)) + (i == segs.count - 1 ? 0.8 : 0.35)
}

let bg = NSColor(calibratedRed: 0.06, green: 0.07, blue: 0.09, alpha: 1)
let accent = NSColor(calibratedRed: 0.35, green: 0.55, blue: 1.0, alpha: 1)
let captionTop: CGFloat = 175  // caption band height from the bottom
let imgRect = CGRect(x: 70, y: captionTop, width: CGFloat(W) - 140, height: CGFloat(H) - captionTop - 70)

func text(_ s: String, size: CGFloat, weight: NSFont.Weight, color: NSColor, in r: CGRect, align: NSTextAlignment = .center) {
    let p = NSMutableParagraphStyle(); p.alignment = align
    let a: [NSAttributedString.Key: Any] = [.font: NSFont.systemFont(ofSize: size, weight: weight), .foregroundColor: color, .paragraphStyle: p]
    let str = NSAttributedString(string: s, attributes: a)
    let h = str.boundingRect(with: r.size, options: [.usesLineFragmentOrigin]).height
    str.draw(with: CGRect(x: r.minX, y: r.midY - h / 2, width: r.width, height: h), options: [.usesLineFragmentOrigin])
}

func fitted(_ img: NSImage, in r: CGRect) -> CGRect {
    let s = min(r.width / img.size.width, r.height / img.size.height)
    let w = img.size.width * s, h = img.size.height * s
    return CGRect(x: r.midX - w / 2, y: r.midY - h / 2, width: w, height: h)
}

func drawShot(_ file: String) -> CGRect {
    let img = NSImage(contentsOf: caps.appendingPathComponent(file))!
    let r = fitted(img, in: imgRect)
    NSGraphicsContext.saveGraphicsState()
    let sh = NSShadow(); sh.shadowBlurRadius = 30; sh.shadowColor = NSColor.black.withAlphaComponent(0.6); sh.set()
    NSBezierPath(roundedRect: r, xRadius: 14, yRadius: 14).fill()
    NSGraphicsContext.restoreGraphicsState()
    NSGraphicsContext.saveGraphicsState()
    NSBezierPath(roundedRect: r, xRadius: 14, yRadius: 14).addClip()
    img.draw(in: r)
    NSGraphicsContext.restoreGraphicsState()
    return r
}

func avatarPlaceholder(center c: CGPoint, radius rad: CGFloat, label: String, sub: String?) {
    let circle = NSBezierPath(ovalIn: CGRect(x: c.x - rad, y: c.y - rad, width: rad * 2, height: rad * 2))
    NSColor(calibratedWhite: 0.16, alpha: 1).setFill(); circle.fill()
    accent.setStroke(); circle.lineWidth = max(4, rad / 40)
    circle.setLineDash([rad / 8, rad / 14], count: 2, phase: 0); circle.stroke()
    text(label, size: rad / 5.5, weight: .bold, color: .white, in: CGRect(x: c.x - rad, y: c.y - rad / 4, width: rad * 2, height: rad / 2))
    if let sub = sub {
        text(sub, size: rad / 10, weight: .regular, color: NSColor(white: 0.7, alpha: 1), in: CGRect(x: c.x - rad, y: c.y - rad / 2, width: rad * 2, height: rad / 4))
    }
}

func render(_ seg: Seg, start: Double, end: Double, into ctx: CGContext) {
    NSGraphicsContext.saveGraphicsState()
    NSGraphicsContext.current = NSGraphicsContext(cgContext: ctx, flipped: false)
    bg.setFill(); CGRect(x: 0, y: 0, width: W, height: H).fill()
    text(TITLE, size: 22, weight: .medium, color: NSColor(white: 0.55, alpha: 1),
         in: CGRect(x: 70, y: CGFloat(H) - 55, width: 1200, height: 34), align: .left)

    switch seg.kind {
    case .avatar:
        avatarPlaceholder(center: CGPoint(x: CGFloat(W) / 2, y: imgRect.midY + 10), radius: 300,
                          label: "YOUR AVATAR CLIP", sub: String(format: "Full frame · %.1fs–%.1fs", start, end))
    case .shot(let f):
        let r = drawShot(f)
        if let note = seg.note {
            let pill = CGRect(x: r.maxX - 560, y: r.maxY - 70, width: 530, height: 50)
            NSColor(calibratedRed: 1, green: 0.8, blue: 0.2, alpha: 0.95).setFill()
            NSBezierPath(roundedRect: pill, xRadius: 25, yRadius: 25).fill()
            text(note, size: 22, weight: .bold, color: .black, in: pill)
        }
    case .outro(let f):
        let r = drawShot(f)
        NSColor.black.withAlphaComponent(0.35).setFill(); NSBezierPath(roundedRect: r, xRadius: 14, yRadius: 14).fill()
        avatarPlaceholder(center: CGPoint(x: r.maxX - 190, y: r.minY + 190), radius: 150, label: "AVATAR", sub: "corner bubble")
    }

    text(seg.caption, size: 50, weight: .semibold, color: .white,
         in: CGRect(x: 120, y: 30, width: CGFloat(W) - 240, height: captionTop - 50))
    NSGraphicsContext.restoreGraphicsState()
}

// 1) Silent video.
let silent = root.appendingPathComponent("build/silent.mp4")
let out = root.appendingPathComponent(OUTPUT)
try? FileManager.default.removeItem(at: silent)
try? FileManager.default.removeItem(at: out)

let writer = try! AVAssetWriter(outputURL: silent, fileType: .mp4)
let input = AVAssetWriterInput(mediaType: .video, outputSettings: [
    AVVideoCodecKey: AVVideoCodecType.h264, AVVideoWidthKey: W, AVVideoHeightKey: H,
    AVVideoCompressionPropertiesKey: [AVVideoAverageBitRateKey: 8_000_000],
])
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: input, sourcePixelBufferAttributes: [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32ARGB, kCVPixelBufferWidthKey as String: W, kCVPixelBufferHeightKey as String: H,
])
writer.add(input)
writer.startWriting()
writer.startSession(atSourceTime: .zero)

var frame: Int64 = 0
var t = 0.0
var starts: [Double] = []
for (i, seg) in segs.enumerated() {
    starts.append(t)
    let endT = t + durations[i]
    var pb: CVPixelBuffer?
    CVPixelBufferPoolCreatePixelBuffer(nil, adaptor.pixelBufferPool!, &pb)
    let buf = pb!
    CVPixelBufferLockBaseAddress(buf, [])
    let ctx = CGContext(data: CVPixelBufferGetBaseAddress(buf), width: W, height: H, bitsPerComponent: 8,
                        bytesPerRow: CVPixelBufferGetBytesPerRow(buf), space: CGColorSpaceCreateDeviceRGB(),
                        bitmapInfo: CGImageAlphaInfo.noneSkipFirst.rawValue)!
    render(seg, start: t, end: endT, into: ctx)
    CVPixelBufferUnlockBaseAddress(buf, [])
    let lastFrame = Int64((endT * Double(fps)).rounded())
    while frame < lastFrame {
        while !input.isReadyForMoreMediaData { usleep(1000) }
        adaptor.append(buf, withPresentationTime: CMTime(value: frame, timescale: fps))
        frame += 1
    }
    t = endT
}
input.markAsFinished()
let done = DispatchSemaphore(value: 0)
writer.finishWriting { done.signal() }
done.wait()
print("silent video: \(String(format: "%.2f", t))s, \(frame) frames")

// 2) Lay the narration clips at each segment start and export.
let comp = AVMutableComposition()
let vAsset = AVURLAsset(url: silent)
let vTrack = comp.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid)!
try! vTrack.insertTimeRange(CMTimeRange(start: .zero, duration: vAsset.duration), of: vAsset.tracks(withMediaType: .video)[0], at: .zero)
let aTrack = comp.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid)!
for (i, seg) in segs.enumerated() {
    let a = AVURLAsset(url: audioURL(seg.audio))
    try! aTrack.insertTimeRange(CMTimeRange(start: .zero, duration: a.duration), of: a.tracks(withMediaType: .audio)[0],
                                at: CMTime(seconds: starts[i] + 0.1, preferredTimescale: 600))
}
let export = AVAssetExportSession(asset: comp, presetName: AVAssetExportPresetHighestQuality)!
export.outputURL = out
export.outputFileType = .mp4
export.exportAsynchronously { done.signal() }
done.wait()
print("export: \(export.status == .completed ? "ok" : "FAILED \(String(describing: export.error))") -> \(out.path)")
for (i, s) in segs.enumerated() { print(String(format: "%d  %5.2f–%5.2f  %@", i + 1, starts[i], starts[i] + durations[i], s.caption)) }
