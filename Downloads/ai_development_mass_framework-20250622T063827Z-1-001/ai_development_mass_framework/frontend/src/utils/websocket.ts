export class OrchestrationWebSocket {
  private ws: WebSocket | null = null;
  private listeners: ((data: any) => void)[] = [];

  connect(clientId: string) {
    this.ws = new WebSocket(`ws://${window.location.hostname}:8000/ws/${clientId}`);
    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      this.listeners.forEach((cb) => cb(data));
    };
  }

  onMessage(cb: (data: any) => void) {
    this.listeners.push(cb);
  }

  send(data: any) {
    if (this.ws && this.ws.readyState === WebSocket.OPEN) {
      this.ws.send(JSON.stringify(data));
    }
  }

  close() {
    if (this.ws) this.ws.close();
  }
}
