# Performance Optimization

This topic explains what grab strategies are and why they are important.

Industrial cameras often produce images at a constant and potentially very high rate (e.g., 60--200 or more fps). In many applications, processing pipelines, like Python, OpenCV, AI inference, etc., can't keep up with this rate.

This creates a fundamental mismatch:

```PlainText
Camera (Producer) → fast
Application (Consumer) → slower
```

Without a grab strategy, one of these situations will arise:

- Buffers grow indefinitely: not possible
- Buffers overflow randomly: undesirable

Grab strategies define **how the system behaves under load**.

## Mental Model

```PlainText
Camera → Frame Stream → Buffer Queue → RetrieveResult() → Application
```

If the application is slower than the camera, the queue fills up and a decision is required how to handle the situation. This is what a grab strategy is for.

## Grab Strategies

Two grab strategies are available.

##### LatestImageOnly

Only the most recent frame is kept. Older frames are dropped while the application is busy. This visualization illustrates this:

```PlainText
Camera:    F1 → F2 → F3 → F4
App reads:        →    F4
Dropped:   F1, F2, F3
```

**Advantages:**

- You always see the most recent state.
- Minimal latency

**Disadvantages:**

- Frame loss

**Typical Use Cases:**

Use **LatestImageOnly** when you need current information, frame drops are acceptable, and latency must be kept to a minimum. Examples:

- Live display (GUI)
- Operator monitoring
- Real-time visualization

##### OneByOne

Every frame is queued and processed in order. No frames are dropped intentionally. This visualization illustrates this:

```PlainText
Camera:    F1 → F2 → F3 → F4
App reads: F1 → F2 → F3 → F4
```

**Advantages:**

- No frame loss (ideal for analysis/recording)
- Deterministic processing order

**Disadvantages:**

- Higher latency if processing is slow
- Risk of buffer overflow with sustained overload

**Typical Use Cases:**

Use **OneByOne** when every frame matters, results must be reproducible, and processing speed is roughly the same as acquisition speed. Examples:

- Inspection systems
- Image recording
- Measurement tasks

## Buffer Configuration

Buffers act as a temporary reservoir between camera and application. You can adjust the number of buffers used as required.

```Python
camera.MaxNumBuffer.Value = 20
```

Increasing the number of buffers has the following advantages:

- Temporary slowdowns are tolerated.

The disadvantages are:

- Memory usage increases.
- Latency increases, i.e., the queue grows.

## Key Takeaways

There is no "best" strategy. The choice depends on whether you need the **latest** image always or **all** images. The following table may serve as guidance for choosing the right strategy.

| Strategy        | Latency        | Frame Loss | Determinism |
| --------------- | -------------- | ---------- | ----------- |
| LatestImageOnly | Low            | Yes        | Low         |
| OneByOne        | High (if slow) | No         | High        |
