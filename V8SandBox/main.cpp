#include <iostream>
#include "main.h"

using namespace v8;
int main(int argc, char* argv[]) {
    // Initialize V8.
    V8::InitializeICUDefaultLocation(argv[0]);
    V8::InitializeExternalStartupData(argv[0]);
    auto platform = platform::NewDefaultPlatform();
    V8::InitializePlatform(platform.get());
    V8::Initialize();
    // Create a new Isolate and make it the current one.
    Isolate::CreateParams create_params;
    create_params.array_buffer_allocator =
        v8::ArrayBuffer::Allocator::NewDefaultAllocator();
    Isolate* isolate = Isolate::New(create_params);
    {
        Isolate::Scope isolate_scope(isolate);
        // Create a stack-allocated handle scope.
        HandleScope handle_scope(isolate);
        // Create a new context.
        Local<Context> context = Context::New(isolate);
        // Enter the context for compiling and running the hello world script.
        Context::Scope context_scope(context);
        // Create a string containing the JavaScript source code.
        Local<String> source =
            String::NewFromUtf8(isolate, "'Hello' + ', World!'",
                NewStringType::kNormal).ToLocalChecked();
        // Compile the source code.
        Local<Script> script = Script::Compile(context, source).ToLocalChecked();
        // Run the script to get the result.
        Local<Value> result = script->Run(context).ToLocalChecked();
        // Convert the result to an UTF8 string and print it.
        String::Utf8Value utf8(isolate, result);
        printf("%s\n", *utf8);
    }
    // Dispose the isolate and tear down V8.
    isolate->Dispose();
    V8::Dispose();
    V8::ShutdownPlatform();
    //delete platform;
    delete create_params.array_buffer_allocator;
    return 0;
}