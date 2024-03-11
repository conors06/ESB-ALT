<script lang="ts">
    import { Button } from "$lib/components/ui/button/index.js";
    import * as Drawer from "$lib/components/ui/drawer/index.js";
    import * as Resizable from "$lib/components/ui/resizable";
  
   
   
  
  </script>
   
  <Drawer.Root>
    <Drawer.Trigger asChild let:builder>
      <Button builders={[builder]} variant="outline">Open Drawer</Button>
    </Drawer.Trigger>
    <Drawer.Content>
      <div class="mx-auto w-full max-w-sm">
        <Drawer.Header>
          <Drawer.Title>Docs</Drawer.Title>
          <Drawer.Description>More Docs.</Drawer.Description>
        </Drawer.Header>
        <Resizable.PaneGroup
    direction="horizontal"
    class="min-h-[200px] max-w-md rounded-lg border"
  >
    <Resizable.Pane defaultSize={50}>
      <div class="flex h-full items-center justify-center p-6">
        <span class="font-semibold">Sidebar</span>
      </div>
    </Resizable.Pane>
    <Resizable.Handle withHandle />
    <Resizable.Pane defaultSize={50}>
      <div class="flex h-full items-center justify-center p-6">
        <span class="font-semibold">Content</span>
      </div>
    </Resizable.Pane>
  </Resizable.PaneGroup>
        <Drawer.Footer>
          <Drawer.Close asChild let:builder>
            <Button builders={[builder]} variant="outline">Cancel</Button>
          </Drawer.Close>
        </Drawer.Footer>
    </Drawer.Content>
  </Drawer.Root>
  
  