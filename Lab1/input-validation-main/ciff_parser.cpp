// g++ -fPIC -shared -o libciff_parser.so ciff_parser.cpp

#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cstdint>

using namespace std;

struct Pixel
{
    unsigned char r, g, b;
    Pixel(unsigned char red, unsigned char green, unsigned char blue)
        : r(red), g(green), b(blue) {}
    Pixel() : r(0), g(0), b(0) {}
};

class CIFF
{
private:
    string _magic;
    long long _header_size;
    long long _content_size;
    long long _width;
    long long _height;
    string _caption;
    vector<string> _tags;
    vector<Pixel> _pixels;
    bool _is_valid;

public:
    // Constructor
    CIFF()
    {
        _magic = "CIFF";
        _header_size = 0;
        _content_size = 0;
        _width = 0;
        _height = 0;
        _caption = "";
        _is_valid = true;
    }

    // Getters
    bool is_valid() const { return _is_valid; }
    const string &magic() const { return _magic; }
    long long header_size() const { return _header_size; }
    long long content_size() const { return _content_size; }
    long long width() const { return _width; }
    long long height() const { return _height; }
    const string &caption() const { return _caption; }
    const vector<string> &tags() const { return _tags; }
    const vector<Pixel> &pixels() const { return _pixels; }

    // Setters
    void set_is_valid(bool value) { _is_valid = value; }
    void set_magic(const string &value) { _magic = value; }
    void set_header_size(long long value) { _header_size = value; }
    void set_content_size(long long value) { _content_size = value; }
    void set_width(long long value) { _width = value; }
    void set_height(long long value) { _height = value; }
    void set_caption(const string &value) { _caption = value; }
    void set_tags(const vector<string> &value) { _tags = value; }
    void set_pixels(const vector<Pixel> &value) { _pixels = value; }

    static CIFF *parse_ciff_file(const string &file_path);
};

CIFF *CIFF::parse_ciff_file(const string &file_path)
{
    CIFF *new_ciff = new CIFF();
    size_t bytes_read = 0;

    try
    {
        ifstream ciff_file(file_path.c_str(), ios::binary);
        if (!ciff_file.is_open())
        {
            throw runtime_error("Cannot open file");
        }

        // Read magic bytes
        char magic[5] = {0};
        ciff_file.read(magic, 4);
        if (ciff_file.gcount() != 4)
        {
            throw runtime_error("Magic must contain 4 bytes!");
        }
        bytes_read += 4;
        new_ciff->set_magic(string(magic, 4));
        if (new_ciff->magic() != "CIFF")
        {
            throw runtime_error("Invalid magic characters!");
        }

        // Read header size
        long long h_size;
        ciff_file.read(reinterpret_cast<char *>(&h_size), 8);
        if (ciff_file.gcount() != 8)
        {
            throw runtime_error("Header size must contain 8 bytes!");
        }
        bytes_read += 8;
        new_ciff->set_header_size(h_size);
        if (new_ciff->header_size() < 38)
        {
            throw runtime_error("Invalid header size!");
        }

        // Read content size
        long long c_size;
        ciff_file.read(reinterpret_cast<char *>(&c_size), 8);
        if (ciff_file.gcount() != 8)
        {
            throw runtime_error("Content size must contain 8 bytes!");
        }
        bytes_read += 8;
        new_ciff->set_content_size(c_size);
        if (new_ciff->content_size() < 0)
        {
            throw runtime_error("Invalid content size!");
        }

        // Read width
        long long width;
        ciff_file.read(reinterpret_cast<char *>(&width), 8);
        if (ciff_file.gcount() != 8)
        {
            throw runtime_error("Width must contain 8 bytes!");
        }
        bytes_read += 8;
        new_ciff->set_width(width);
        if (new_ciff->width() < 0)
        {
            throw runtime_error("Invalid width!");
        }

        // Read height
        long long height;
        ciff_file.read(reinterpret_cast<char *>(&height), 8);
        if (ciff_file.gcount() != 8)
        {
            throw runtime_error("Height must contain 8 bytes!");
        }
        bytes_read += 8;
        new_ciff->set_height(height);
        if (new_ciff->height() < 0)
        {
            throw runtime_error("Invalid height!");
        }

        if (new_ciff->content_size() != new_ciff->width() * new_ciff->height() * 3)
        {
            throw runtime_error("Invalid content size!");
        }

        // Read caption
        string caption;
        char c;
        while (true)
        {
            ciff_file.read(&c, 1);
            if (ciff_file.gcount() != 1)
            {
                throw runtime_error("Invalid image");
            }
            bytes_read += 1;

            if (c == '\n')
            {
                break;
            }

            caption += c;
        }
        new_ciff->set_caption(caption);

        // Read tags
        vector<string> tags;
        string tag;

        while (bytes_read < new_ciff->header_size())
        {
            ciff_file.read(&c, 1);
            if (ciff_file.gcount() != 1)
            {
                throw runtime_error("Invalid image");
            }
            bytes_read += 1;

            if (c == '\n')
            {
                throw runtime_error("Invalid image");
            }

            tag += c;
            if (c == '\0')
            {
                tags.push_back(tag);
                tag = "";
            }

            if (bytes_read == new_ciff->header_size() && c != '\0')
            {
                throw runtime_error("Invalid image");
            }
        }

        for (int i = 0; i < tags.size(); i++)
        {
            if (tags[i].empty())
            {
                throw runtime_error("Invalid image");
            }
        }
        new_ciff->set_tags(tags);

        // Read pixels
        vector<Pixel> pixels;
        unsigned long pixel_count = static_cast<unsigned long>(new_ciff->width()) *
                                    static_cast<unsigned long>(new_ciff->height());

        for (unsigned long i = 0; i < pixel_count && !ciff_file.eof(); ++i)
        {
            unsigned char pixel[3];
            ciff_file.read(reinterpret_cast<char *>(pixel), 3);
            if (ciff_file.gcount() != 3)
            {
                throw runtime_error("Invalid image");
            }
            bytes_read += 3;
            pixels.push_back(Pixel(pixel[0], pixel[1], pixel[2]));
        }

        new_ciff->set_pixels(pixels);
        ciff_file.read(&c, 1);
        if (!ciff_file.eof())
        {
            throw runtime_error("Invalid image");
        }
    }
    catch (const exception &e)
    {
        new_ciff->set_is_valid(false);
        cerr << "Error: " << e.what() << endl;
    }

    return new_ciff;
}

// Create a C interface for Python to use
extern "C"
{
    void *parse_ciff(const char *file_path)
    {
        try
        {
            CIFF *ciff = CIFF::parse_ciff_file(string(file_path));
            return static_cast<void *>(ciff);
        }
        catch (...)
        {
            return NULL;
        }
    }

    bool get_is_valid(void *ciff_ptr)
    {
        if (!ciff_ptr)
        {
            return false;
        }
        CIFF *ciff = static_cast<CIFF *>(ciff_ptr);
        return ciff->is_valid();
    }

    const char *get_magic(void *ciff_ptr)
    {
        CIFF *ciff = static_cast<CIFF *>(ciff_ptr);
        if (!ciff->is_valid())
        {
            return NULL;
        }
        return ciff->magic().c_str();
    }

    long long get_header_size(void *ciff_ptr)
    {
        CIFF *ciff = static_cast<CIFF *>(ciff_ptr);
        return ciff->header_size();
    }

    long long get_content_size(void *ciff_ptr)
    {
        CIFF *ciff = static_cast<CIFF *>(ciff_ptr);
        return ciff->content_size();
    }

    long long get_width(void *ciff_ptr)
    {
        CIFF *ciff = static_cast<CIFF *>(ciff_ptr);
        return ciff->width();
    }

    long long get_height(void *ciff_ptr)
    {
        CIFF *ciff = static_cast<CIFF *>(ciff_ptr);
        return ciff->height();
    }

    const char *get_caption(void *ciff_ptr)
    {
        CIFF *ciff = static_cast<CIFF *>(ciff_ptr);
        if (!ciff->is_valid())
        {
            return NULL;
        }
        return ciff->caption().c_str();
    }

    void free_ciff(void *ciff_ptr)
    {
        if (ciff_ptr)
        {
            CIFF *ciff = static_cast<CIFF *>(ciff_ptr);
            delete ciff;
        }
    }
}

// Main function for testing
int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        cerr << "Usage: " << argv[0] << " <ciff_file_path>" << endl;
        return 1;
    }

    string file_path = argv[1];
    CIFF *ciff = CIFF::parse_ciff_file(file_path);

    if (ciff->is_valid())
    {
        cout << file_path << "\t is detected as \tVALID" << endl;
    }
    else
    {
        cout << file_path << "\t is detected as \tINVALID" << endl;
    }

    delete ciff;
    return 0;
}